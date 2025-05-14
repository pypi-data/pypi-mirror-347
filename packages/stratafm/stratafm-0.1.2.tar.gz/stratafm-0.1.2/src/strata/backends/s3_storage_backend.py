import io
import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from strata.backends.storage_backend import StorageBackend
from strata.entities import Content, File, FileType
from strata.exceptions import BackendException, NotFoundException

# # Circuit breaker and retries config
# self.CB_FAIL_MAX: int = self.get_env_variable("CB_FAIL_MAX", 5)
# self.CB_RESET_TIMEOUT: int = self.get_env_variable("CB_RESET_TIMEOUT", 60)
# self.MAX_ATTEMPTS: int = self.get_env_variable("MAX_ATTEMPTS", 5)
# self.MAX_RETRIES: int = self.get_env_variable("MAX_RETRIES", 5)


class S3StorageBackend(StorageBackend):
    def __init__(self, config: dict[str, str]):
        # Validate required parameters
        if "bucket_name" not in config:
            raise BackendException("Missing required parameter 'bucket_name'")

        self.bucket_name = config.get("bucket_name")
        self.base_prefix = config.get("base_prefix", "")

        # Initialize the S3 client
        try:
            # Create S3 client without explicit credentials - boto3 will automatically
            # use credentials from environment variables or AWS configuration files
            self.s3_client = boto3.client("s3")

            # Quick validation that we can access the bucket
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except Exception as e:
            raise BackendException(f"Failed to initialize S3 client: {str(e)}")

    async def list(self, path: str, depth: int = 1) -> list[File]:
        try:
            full_path = self._get_full_path(path)

            # Ensure the path ends with a slash if it's not empty
            if full_path and not full_path.endswith("/"):
                full_path += "/"

            # List objects in S3 with the specified prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=full_path,
                Delimiter="/"
                if depth <= 1
                else None,  # Use delimiter for non-recursive listing
            )

            result = []

            # Process directories (CommonPrefixes)
            for prefix in response.get("CommonPrefixes", []):
                prefix_path = prefix.get("Prefix")
                name = os.path.basename(prefix_path.rstrip("/"))
                relative_path = self._get_relative_path(prefix_path)

                file_obj = File(
                    name=name,
                    path=relative_path,
                    type=FileType.directory,
                    modified=None,  # S3 doesn't provide modified date for prefixes
                    size=None,
                    children=None
                )

                # If depth > 1, recurse into subdirectories
                if depth > 1:
                    children = await self.list(relative_path, depth - 1)
                    file_obj.children = children

                result.append(file_obj)

            # Process files (Contents)
            for content in response.get("Contents", []):
                # Skip entries that represent directories themselves
                key = content.get("Key")
                if key == full_path or key.endswith("/"):
                    continue

                name = os.path.basename(key)
                relative_path = self._get_relative_path(key)

                file_obj = File(
                    name=name,
                    path=relative_path,
                    type=FileType.file,
                    size=content.get("Size"),
                    modified=content.get("LastModified"),
                    children=None
                )

                result.append(file_obj)

            return result
        except ClientError as e:
            raise BackendException(f"S3 error listing path {path}: {str(e)}")
        except Exception as e:
            raise BackendException(f"Error listing directory {path}: {str(e)}")

    async def view(self, path: str) -> Content:
        try:
            full_path = self._get_full_path(path)

            # Get the object from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=full_path)

            # Read content and convert to appropriate format
            file_content = response["Body"].read()
            content_type = response.get("ContentType", "application/octet-stream")

            return Content(
                content=file_content,
                content_type=content_type,
                children=None
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise NotFoundException(message=f"File not found: {path}", path=path)
            raise BackendException(f"S3 error viewing file {path}: {str(e)}")
        except Exception as e:
            raise BackendException(f"Error viewing file {path}: {str(e)}")

    async def create_file(self, path: str, content: bytes) -> File:
        try:
            full_path = self._get_full_path(path)

            # Upload the file to S3
            self.s3_client.upload_fileobj(
                io.BytesIO(content), self.bucket_name, full_path
            )

            # Get object information
            response = self.s3_client.head_object(
                Bucket=self.bucket_name, Key=full_path
            )

            # Return File object with metadata
            return File(
                name=os.path.basename(path),
                path=path,
                type=FileType.file,
                size=response.get("ContentLength"),
                modified=response.get("LastModified"),
            )
        except ClientError as e:
            raise BackendException(f"S3 error creating file {path}: {str(e)}")
        except Exception as e:
            raise BackendException(f"Error creating file {path}: {str(e)}")

    async def create_directory(self, path: str) -> File:
        try:
            # In S3, directories are just prefixes, so we create an empty object with a trailing slash
            full_path = self._get_full_path(path)
            if not full_path.endswith("/"):
                full_path += "/"

            # Create empty directory marker
            self.s3_client.put_object(Bucket=self.bucket_name, Key=full_path, Body=b"")

            # Return the directory object
            now = datetime.now()
            return File(
                name=os.path.basename(path),
                path=path,
                type=FileType.directory,
                modified=now,
                size=None,
                children=None
            )
        except ClientError as e:
            raise BackendException(f"S3 error creating directory {path}: {str(e)}")
        except Exception as e:
            raise BackendException(f"Error creating directory {path}: {str(e)}")

    async def delete(self, path: str, recursive: bool = False) -> None:
        try:
            full_path = self._get_full_path(path)

            # Check if path exists
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=full_path)
                # It's a file, delete it
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=full_path)
                return
            except ClientError as e:
                if e.response["Error"]["Code"] != "404":
                    raise e

            # If we get here, it might be a directory
            if not full_path.endswith("/"):
                full_path += "/"

            # List objects to see if it exists and has content
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=full_path,
                MaxKeys=2,  # Just need to check if there's anything
            )

            if "Contents" not in response:
                raise NotFoundException(message=f"Path not found: {path}", path=path)

            # If not recursive and there are multiple objects, it's not empty
            if not recursive and len(response.get("Contents", [])) > 1:
                raise BackendException(
                    f"Cannot delete non-empty directory without recursive flag: {path}"
                )

            # Delete all objects with this prefix if recursive
            if recursive:
                paginator = self.s3_client.get_paginator("list_objects_v2")
                for page in paginator.paginate(
                    Bucket=self.bucket_name, Prefix=full_path
                ):
                    if "Contents" in page:
                        objects = [{"Key": obj["Key"]} for obj in page["Contents"]]
                        self.s3_client.delete_objects(
                            Bucket=self.bucket_name, Delete={"Objects": objects}
                        )
            else:
                # Just delete the directory marker
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=full_path)

        except ClientError as e:
            raise BackendException(f"S3 error deleting {path}: {str(e)}")
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error deleting {path}: {str(e)}")

    async def move(self, src_path: str, dst_path: str) -> File:
        try:
            # S3 doesn't have a direct move operation, so we'll copy and delete
            file_obj = await self.copy(src_path, dst_path)
            await self.delete(src_path)
            return file_obj
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error moving {src_path} to {dst_path}: {str(e)}")

    async def copy(self, src_path: str, dst_path: str) -> File:
        try:
            full_src_path = self._get_full_path(src_path)
            full_dst_path = self._get_full_path(dst_path)

            # Check if source exists
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=full_src_path)
                # It's a file, copy it
                self.s3_client.copy_object(
                    Bucket=self.bucket_name,
                    CopySource={"Bucket": self.bucket_name, "Key": full_src_path},
                    Key=full_dst_path,
                )

                # Get metadata of the copied file
                response = self.s3_client.head_object(
                    Bucket=self.bucket_name, Key=full_dst_path
                )

                return File(
                    name=os.path.basename(dst_path),
                    path=dst_path,
                    type=FileType.file,
                    size=response.get("ContentLength"),
                    modified=response.get("LastModified"),
                    children=None
                )

            except ClientError as e:
                if e.response["Error"]["Code"] != "404":
                    raise e

            # If we get here, it might be a directory
            if not full_src_path.endswith("/"):
                full_src_path += "/"
            if not full_dst_path.endswith("/"):
                full_dst_path += "/"

            # Copy all objects with this prefix
            paginator = self.s3_client.get_paginator("list_objects_v2")
            for page in paginator.paginate(
                Bucket=self.bucket_name, Prefix=full_src_path
            ):
                if "Contents" in page and page["Contents"]:
                    for obj in page["Contents"]:
                        src_key = obj["Key"]
                        dst_key = full_dst_path + src_key[len(full_src_path) :]

                        self.s3_client.copy_object(
                            Bucket=self.bucket_name,
                            CopySource={"Bucket": self.bucket_name, "Key": src_key},
                            Key=dst_key,
                        )

            # Return directory information
            now = datetime.now()
            return File(
                name=os.path.basename(dst_path.rstrip("/")),
                path=dst_path,
                type=FileType.directory,
                modified=now,
                size=None,
                children=None
            )

        except ClientError as e:
            raise BackendException(
                f"S3 error copying {src_path} to {dst_path}: {str(e)}"
            )
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error copying {src_path} to {dst_path}: {str(e)}")

    def _get_full_path(self, relative_path: str) -> str:
        try:
            # Normalize path by removing leading slashes and handling dots
            normalized_path = os.path.normpath(relative_path).lstrip("/")

            # Protect against directory traversal attacks
            if normalized_path.startswith(".."):
                raise BackendException(
                    f"Path cannot access parent directories: {relative_path}"
                )

            # Join with base prefix if specified
            if self.base_prefix:
                return os.path.join(self.base_prefix, normalized_path)
            return normalized_path
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error processing path {relative_path}: {str(e)}")

    def _get_relative_path(self, full_path: str) -> str:
        """Convert a full S3 key back to a relative path."""
        if self.base_prefix and full_path.startswith(self.base_prefix):
            return full_path[len(self.base_prefix) :].lstrip("/")
        return full_path
