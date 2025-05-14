from enum import Enum
from typing import Dict, List, Optional, Union, Type, Callable, Any

from strata.backends.local_storage_backend import LocalStorageBackend
from strata.backends.s3_storage_backend import S3StorageBackend
from strata.backends.storage_backend import StorageBackend
from strata.entities import Content, File
from strata.exceptions import BackendException
from strata.logging import logger


class BackendType(str, Enum):
    """Enumeration of supported backend types."""

    LOCAL = "local"
    S3 = "s3"
    # You can add more backend types here in the future


class FileManager:
    """
    Main class that manages file operations across different backends.

    This class serves as a facade for all storage operations,
    delegating to the appropriate backend according to the configuration.
    """

    # Static dictionary mapping backend types to their respective classes
    _backend_classes: Dict[str, Type[StorageBackend]] = {
        BackendType.LOCAL: LocalStorageBackend,
        BackendType.S3: S3StorageBackend,
    }

    def __init__(self) -> None:
        self.backends: Dict[str, StorageBackend] = {}
        self.default_backend: Optional[str] = None

    def register_backend(
        self, name: str, backend: StorageBackend, set_as_default: bool = False
    ) -> None:
        """
        Register a storage backend with a specific name.

        Args:
            name: Unique identifier for this backend
            backend: Instance of the storage backend
            set_as_default: Whether to set as the default backend
        """
        self.backends[name] = backend
        if set_as_default or self.default_backend is None:
            self.default_backend = name

    @classmethod
    def register_backend_class(
        cls, backend_type: str, backend_class: Type[StorageBackend]
    ) -> None:
        """
        Register a new backend class to create instances dynamically.

        Args:
            backend_type: Identifier for the backend type (e.g., "azure")
            backend_class: Backend class to register
        """
        cls._backend_classes[backend_type] = backend_class

    @classmethod
    def create_backend(cls, backend_type: str, config: Dict[str, Any]) -> StorageBackend:
        """
        Create a backend instance based on the specified type.

        Args:
            backend_type: Type of backend to create (local, s3, etc.)
            config: Configuration specific to the backend

        Returns:
            Storage backend instance

        Raises:
            BackendException: If the backend type is not supported
        """
        backend_class = cls._backend_classes.get(backend_type)

        if backend_class is None:
            raise BackendException(f"Backend type '{backend_type}' not supported")

        return backend_class(config)  # Las clases backend deben aceptar el config dict

    @classmethod
    def from_config(cls, config: Dict[str, Any] | List[Dict[str, Any]]) -> "FileManager":
        """
        Create a FileManager from a configuration.

        Args:
            config: Configuration for one or multiple backends

        Returns:
            Configured FileManager instance
        """
        manager = cls()

        # If it's a single backend
        if isinstance(config, dict):
            configs = [config]
        else:
            configs = config

        for backend_config in configs:
            backend_type = backend_config.pop("type", None)
            name = backend_config.pop("name", backend_type)
            set_default = backend_config.pop("default", False)

            if not backend_type:
                raise BackendException("Backend configuration must include 'type'")

            backend = cls.create_backend(backend_type, backend_config)
            manager.register_backend(name, backend, set_default)

        logger.debug(f"FileManager created with backends: {manager.backends.keys()}")

        return manager

    def _get_backend(self, backend_name: Optional[str] = None) -> StorageBackend:
        """
        Get a backend by name or the default backend.

        Args:
            backend_name: Name of the backend to use

        Returns:
            Storage backend

        Raises:
            BackendException: If the backend is not found
        """
        name = backend_name or self.default_backend

        if not name or name not in self.backends:
            raise BackendException(f"Backend '{name}' not found")

        return self.backends[name]

    # Methods that replicate the StorageBackend interface
    # but delegate to the specific backend

    async def list(
        self, path: str, depth: int = 1, backend: Optional[str] = None
    ) -> List[File]:
        """
        List files and directories in the specified path.

        Args:
            path: Path to list
            depth: Recursion depth for directories
            backend: Backend to use (optional)

        Returns:
            List of File objects
        """
        logger.debug(
            f"Listing path '{path}' with depth {depth} on backend '{backend or self.default_backend}'"
        )

        storage = self._get_backend(backend)

        return await storage.list(path, depth)

    async def view(self, path: str, backend: Optional[str] = None) -> Content:
        """
        Get the content of a file.

        Args:
            path: File path
            backend: Backend to use (optional)

        Returns:
            File content
        """

        logger.debug(
            f"Viewing file '{path}' on backend '{backend or self.default_backend}'"
        )

        storage = self._get_backend(backend)
        return await storage.view(path)

    async def create_file(
        self, path: str, content: bytes, backend: Optional[str] = None
    ) -> File:
        """
        Create a new file.

        Args:
            path: Path of the file to create
            content: Content in bytes
            backend: Backend to use (optional)

        Returns:
            Created File object
        """

        logger.debug(
            f"Creating file '{path}' on backend '{backend or self.default_backend}'"
        )
        if not isinstance(content, bytes):
            raise ValueError("Content must be of type bytes")

        storage = self._get_backend(backend)
        return await storage.create_file(path, content)

    async def create_directory(self, path: str, backend: Optional[str] = None) -> File:
        """
        Create a new directory.

        Args:
            path: Path of the directory to create
            backend: Backend to use (optional)

        Returns:
            File object representing the directory
        """

        logger.debug(
            f"Creating directory '{path}' on backend '{backend or self.default_backend}'"
        )

        storage = self._get_backend(backend)
        return await storage.create_directory(path)

    async def delete(
        self, path: str, recursive: bool = False, backend: Optional[str] = None
    ) -> None:
        """
        Delete a file or directory.

        Args:
            path: Path to delete
            recursive: Whether to delete recursively (for directories)
            backend: Backend to use (optional)
        """

        logger.debug(
            f"Deleting path '{path}' on backend '{backend or self.default_backend}'"
        )

        storage = self._get_backend(backend)
        await storage.delete(path, recursive)

    async def move(
        self,
        src_path: str,
        dst_path: str,
        src_backend: Optional[str] = None,
        dst_backend: Optional[str] = None,
    ) -> File:
        """
        Move a file or directory.

        Args:
            src_path: Source path
            dst_path: Destination path
            src_backend: Source backend (optional)
            dst_backend: Destination backend (optional)

        Returns:
            File object in its new location

        Note:
            If src_backend and dst_backend are different, performs a cross-backend copy
            and then deletes the original.
        """

        logger.debug(
            f"Moving from '{src_path}' to '{dst_path}' on backends '{src_backend or self.default_backend}' and '{dst_backend or self.default_backend}'"
        )

        if src_backend == dst_backend or (src_backend is None and dst_backend is None):
            # Operation within the same backend
            storage = self._get_backend(src_backend)
            return await storage.move(src_path, dst_path)
        else:
            # Operation between different backends
            src_storage = self._get_backend(src_backend)
            dst_storage = self._get_backend(dst_backend)

            # For files
            content = await src_storage.view(src_path)
            result = await dst_storage.create_file(dst_path, content.content)
            await src_storage.delete(src_path)
            return result

    async def copy(
        self,
        src_path: str,
        dst_path: str,
        src_backend: Optional[str] = None,
        dst_backend: Optional[str] = None,
    ) -> File:
        """
        Copy a file or directory.

        Args:
            src_path: Source path
            dst_path: Destination path
            src_backend: Source backend (optional)
            dst_backend: Destination backend (optional)

        Returns:
            File object in its new location

        Note:
            If src_backend and dst_backend are different, performs a cross-backend copy.
        """

        logger.debug(
            f"Copying from '{src_path}' to '{dst_path}' on backends '{src_backend or self.default_backend}' and '{dst_backend or self.default_backend}'"
        )

        if src_backend == dst_backend or (src_backend is None and dst_backend is None):
            # Operation within the same backend
            storage = self._get_backend(src_backend)
            return await storage.copy(src_path, dst_path)
        else:
            # Operation between different backends
            src_storage = self._get_backend(src_backend)
            dst_storage = self._get_backend(dst_backend)

            # For files
            content = await src_storage.view(src_path)
            return await dst_storage.create_file(dst_path, content.content)
