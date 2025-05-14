import os
from datetime import datetime
from os import listdir, makedirs, stat

from strata.backends.storage_backend import StorageBackend
from strata.entities import Content, File, FileType
from strata.exceptions import BackendException, NotFoundException


class LocalStorageBackend(StorageBackend):
    def __init__(self, config: dict[str, str]):
        if "base_folder" not in config:
            raise BackendException("Missing required parameter 'base_folder'")
        self.base_folder = config.get("base_folder", "")

    async def list(self, path_str: str, depth: int = 1) -> list[File]:
        full_path = self._get_full_path(path_str)

        if not os.path.exists(full_path):
            raise NotFoundException(
                message=f"Path not found: {path_str}", path=path_str
            )

        result = []

        try:
            items = listdir(full_path)
            for item_name in items:
                item_path = os.path.join(full_path, item_name)
                relative_path = os.path.join(path_str, item_name)

                # Get file stats
                stats = stat(item_path)
                is_dir = os.path.isdir(item_path)

                # Create File object with appropriate information
                file_obj = File(
                    name=item_name,
                    path=relative_path,
                    type=FileType.directory if is_dir else FileType.file,
                    size=None if is_dir else stats.st_size,
                    modified=datetime.fromtimestamp(stats.st_mtime),
                    children=None
                )

                # If it's a directory and we need to go deeper, get children
                if is_dir and depth > 1:
                    children = await self.list(relative_path, depth - 1)
                    file_obj.children = children

                result.append(file_obj)

            return result
        except Exception as e:
            raise BackendException(f"Error listing directory {path_str}: {str(e)}")

    async def view(self, path: str) -> Content:
        try:
            full_path = self._get_full_path(path)

            # Check if path exists and is a file
            if not os.path.exists(full_path):
                raise NotFoundException(message=f"Path not found: {path}", path=path)

            if os.path.isdir(full_path):
                raise BackendException(f"Cannot view content of a directory: {path}")

            # Read the file content
            with open(full_path, "rb") as f:
                content_bytes = f.read()

            # Determine content type (simple implementation, could be enhanced)
            content_type = self._guess_content_type(full_path)

            # Return Content object
            return Content(
                file=os.path.basename(path),
                content=content_bytes,
                content_type=content_type,
            )
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error viewing file {path}: {str(e)}")

    def _guess_content_type(self, file_path: str) -> str:
        """Simple function to guess content type based on file extension."""
        import mimetypes

        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or "application/octet-stream"

    async def create_file(self, path: str, content: bytes) -> File:
        try:
            full_path = self._get_full_path(path)
            # Ensure directory exists
            makedirs(os.path.dirname(full_path), exist_ok=True)

            # Write content to file
            with open(full_path, "wb") as f:
                f.write(content)

            # Get file stats to return accurate metadata
            stats = os.stat(full_path)

            # Return a File object with complete metadata
            return File(
                name=os.path.basename(full_path),
                path=path,  # Return the relative path, not the full path
                type=FileType.file,
                size=stats.st_size,
                modified=datetime.fromtimestamp(stats.st_mtime),
                children=None
            )
        except Exception as e:
            raise BackendException(f"Error creating file {path}: {str(e)}")

    async def create_directory(self, path: str) -> File:
        try:
            full_path = self._get_full_path(path)
            makedirs(full_path, exist_ok=True)

            # Get directory stats
            stats = os.stat(full_path)

            # Return a File object with proper metadata
            return File(
                name=os.path.basename(full_path),
                path=path,  # Return the relative path, not the full path
                type=FileType.directory,
                modified=datetime.fromtimestamp(stats.st_mtime),
                size=None,
                children=None
            )
        except Exception as e:
            raise BackendException(f"Error creating directory {path}: {str(e)}")

    async def delete(self, path: str, recursive: bool = False) -> None:
        try:
            full_path = self._get_full_path(path)

            if not os.path.exists(full_path):
                raise BackendException(f"Path not found: {path}")

            if os.path.isdir(full_path):
                if recursive:
                    # For recursive deletion of directories, use shutil.rmtree
                    import shutil

                    shutil.rmtree(full_path)
                else:
                    # For non-recursive deletion, only delete if directory is empty
                    if os.listdir(full_path):
                        raise BackendException(
                            f"Cannot delete non-empty directory without recursive flag: {path}"
                        )
                    os.rmdir(full_path)
            else:
                # For files, always delete
                os.remove(full_path)

        except BackendException:
            # Re-raise existing BackendExceptions
            raise
        except Exception as e:
            # Wrap other exceptions with BackendException
            raise BackendException(f"Error deleting {path}: {str(e)}")

    async def move(self, src_path: str, dst_path: str) -> File:
        try:
            full_src_path = self._get_full_path(src_path)
            full_dst_path = self._get_full_path(dst_path)

            if not os.path.exists(full_src_path):
                raise NotFoundException(
                    message=f"Source path not found: {src_path}", path=src_path
                )

            # Make sure destination directory exists
            os.makedirs(os.path.dirname(full_dst_path), exist_ok=True)

            # Check if destination exists and is not a directory
            is_dir = os.path.isdir(full_src_path)
            if (
                os.path.exists(full_dst_path)
                and not os.path.isdir(full_dst_path) == is_dir
            ):
                raise BackendException(
                    f"Cannot move: destination exists with different type: {dst_path}"
                )

            # Perform the move operation
            import shutil

            shutil.move(full_src_path, full_dst_path)

            # Get stats of the moved file/directory
            stats = os.stat(full_dst_path)

            # Return File object with correct metadata
            return File(
                name=os.path.basename(full_dst_path),
                path=dst_path,
                type=FileType.directory if is_dir else FileType.file,
                size=None if is_dir else stats.st_size,
                modified=datetime.fromtimestamp(stats.st_mtime),
                children=None
            )
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error moving {src_path} to {dst_path}: {str(e)}")

    async def copy(self, src_path: str, dst_path: str) -> File:
        try:
            full_src_path = self._get_full_path(src_path)
            full_dst_path = self._get_full_path(dst_path)

            if not os.path.exists(full_src_path):
                raise NotFoundException(
                    message=f"Source path not found: {src_path}", path=src_path
                )

            # Make sure destination directory exists
            os.makedirs(os.path.dirname(full_dst_path), exist_ok=True)

            is_dir = os.path.isdir(full_src_path)

            # Perform the copy operation
            import shutil

            if is_dir:
                if os.path.exists(full_dst_path):
                    raise BackendException(
                        f"Destination directory already exists: {dst_path}"
                    )
                shutil.copytree(full_src_path, full_dst_path)
            else:
                shutil.copy2(full_src_path, full_dst_path)

            # Get stats of the copied file/directory
            stats = os.stat(full_dst_path)

            # Return File object with correct metadata
            return File(
                name=os.path.basename(full_dst_path),
                path=dst_path,
                type=FileType.directory if is_dir else FileType.file,
                size=None if is_dir else stats.st_size,
                modified=datetime.fromtimestamp(stats.st_mtime),
                children=None
            )
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error copying {src_path} to {dst_path}: {str(e)}")

    def _get_full_path(self, relative_path: str) -> str:
        try:
            # Normalize path to handle ".." and "." segments
            normalized_path = os.path.normpath(relative_path)

            # Ensure the path doesn't try to access parent directories
            if normalized_path.startswith("..") or normalized_path.startswith("/.."):
                raise BackendException(
                    f"Path cannot access parent directories: {relative_path}"
                )

            # Join with base folder and return absolute path
            return os.path.join(self.base_folder, normalized_path)
        except BackendException:
            raise
        except Exception as e:
            raise BackendException(f"Error processing path {relative_path}: {str(e)})")
