import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
from typing import Dict, List

from strata.file_manager import FileManager, BackendType
from strata.backends.storage_backend import StorageBackend
from strata.entities import File, Content, FileType
from strata.exceptions import BackendException

class TestFileManager:
    @pytest.fixture
    def mock_backend(self):
        """Create a mock storage backend."""
        mock = MagicMock(spec=StorageBackend)
        # Convert methods to AsyncMocks for async testing
        mock.list = AsyncMock()
        mock.view = AsyncMock()
        mock.create_file = AsyncMock()
        mock.create_directory = AsyncMock()
        mock.delete = AsyncMock()
        mock.move = AsyncMock()
        mock.copy = AsyncMock()
        return mock

    @pytest.fixture
    def file_manager(self, mock_backend):
        """Create a FileManager with a mock backend."""
        manager = FileManager()
        manager.register_backend("test_backend", mock_backend, set_as_default=True)
        return manager

    @pytest.fixture
    def sample_file(self):
        """Create a sample File object."""
        return File(
            name="test.txt",
            path="/test/test.txt",
            type=FileType.file,
            size=100,
            modified=None
        )

    @pytest.fixture
    def sample_content(self):
        """Create a sample Content object."""
        return Content(
            file="test.txt",
            content=b"test content",
            content_type="text/plain"
        )

    def test_register_backend(self, mock_backend):
        """Test registering a backend."""
        manager = FileManager()
        
        # Test registering a backend
        manager.register_backend("test_backend", mock_backend)
        assert "test_backend" in manager.backends
        assert manager.default_backend == "test_backend"  # Should be default as it's the first one
        
        # Test registering another backend without making it default
        mock_backend2 = MagicMock(spec=StorageBackend)
        manager.register_backend("test_backend2", mock_backend2, set_as_default=False)
        assert "test_backend2" in manager.backends
        assert manager.default_backend == "test_backend"  # Should still be the first one
        
        # Test registering another backend and making it default
        mock_backend3 = MagicMock(spec=StorageBackend)
        manager.register_backend("test_backend3", mock_backend3, set_as_default=True)
        assert "test_backend3" in manager.backends
        assert manager.default_backend == "test_backend3"  # Should now be the new one

    def test_register_backend_class(self):
        """Test registering a new backend class type."""
        # Create a custom backend class
        class CustomBackend(StorageBackend):
            pass
        
        # Register the custom backend class
        FileManager.register_backend_class("custom", CustomBackend)
        
        # Verify it's registered
        assert "custom" in FileManager._backend_classes
        assert FileManager._backend_classes["custom"] == CustomBackend

    def test_create_backend(self):
        """Test creating a backend from a type."""
        # Mock the backend classes to avoid actual instantiation
        with patch.dict(FileManager._backend_classes, {
            BackendType.LOCAL: MagicMock(return_value="local_instance"),
            BackendType.S3: MagicMock(return_value="s3_instance")
        }):
            # Test creating a local backend
            backend = FileManager.create_backend(BackendType.LOCAL, {"base_folder": "/tmp"})
            assert backend == "local_instance"
            FileManager._backend_classes[BackendType.LOCAL].assert_called_with({"base_folder": "/tmp"})
            
            # Test creating an S3 backend
            backend = FileManager.create_backend(BackendType.S3, {"bucket_name": "test-bucket"})
            assert backend == "s3_instance"
            FileManager._backend_classes[BackendType.S3].assert_called_with({"bucket_name": "test-bucket"})
            
            # Test creating an unsupported backend type
            with pytest.raises(BackendException):
                FileManager.create_backend("unknown_type", {})

    def test_from_config(self):
        """Test creating a FileManager from a configuration."""
        # Mock the create_backend method
        with patch.object(FileManager, 'create_backend') as mock_create:
            # Proporcionar suficientes valores para todas las llamadas
            mock_create.side_effect = ["backend1", "backend2", "backend3"]

            # Test with a single backend config
            config = {
                "type": "local",
                "name": "local_files",
                "base_folder": "/tmp",
                "default": True
            }
            manager = FileManager.from_config(config)
            assert "local_files" in manager.backends
            assert manager.default_backend == "local_files"

            # Test with multiple backend configs
            configs = [
                {
                    "type": "local",
                    "name": "local_storage",
                    "base_folder": "/tmp"
                },
                {
                    "type": "s3",
                    "name": "cloud_storage",
                    "bucket_name": "test-bucket",
                    "default": True
                }
            ]
            manager = FileManager.from_config(configs)
            assert "local_storage" in manager.backends
            assert "cloud_storage" in manager.backends
            assert manager.default_backend == "cloud_storage"
            
            # Test with invalid config (missing type)
            with pytest.raises(BackendException):
                FileManager.from_config({"name": "invalid"})

    def test_get_backend(self, file_manager, mock_backend):
        """Test getting a backend by name or default."""
        # Test getting the default backend
        assert file_manager._get_backend() == mock_backend
        
        # Test getting a backend by name
        assert file_manager._get_backend("test_backend") == mock_backend
        
        # Test getting a non-existent backend
        with pytest.raises(BackendException):
            file_manager._get_backend("nonexistent_backend")
        
        # Test with no default backend set
        file_manager.default_backend = None
        with pytest.raises(BackendException):
            file_manager._get_backend()

    @pytest.mark.asyncio
    async def test_list(self, file_manager, mock_backend, sample_file):
        """Test listing files and directories."""
        # Set up the mock to return a sample result
        mock_backend.list.return_value = [sample_file]
        
        # Test with default backend
        result = await file_manager.list("/test", depth=2)
        mock_backend.list.assert_called_once_with("/test", 2)
        assert result == [sample_file]
        
        # Test with specified backend
        mock_backend.list.reset_mock()
        result = await file_manager.list("/test", backend="test_backend")
        mock_backend.list.assert_called_once_with("/test", 1)
        assert result == [sample_file]

    @pytest.mark.asyncio
    async def test_view(self, file_manager, mock_backend, sample_content):
        """Test viewing a file's content."""
        # Set up the mock to return a sample content
        mock_backend.view.return_value = sample_content
        
        # Test viewing a file
        result = await file_manager.view("/test/test.txt")
        mock_backend.view.assert_called_once_with("/test/test.txt")
        assert result == sample_content

    @pytest.mark.asyncio
    async def test_create_file(self, file_manager, mock_backend, sample_file):
        """Test creating a file."""
        # Set up the mock to return a sample file
        mock_backend.create_file.return_value = sample_file
        
        # Test creating a file
        result = await file_manager.create_file("/test/new.txt", b"content")
        mock_backend.create_file.assert_called_once_with("/test/new.txt", b"content")
        assert result == sample_file
        
        # Test with non-bytes content
        with pytest.raises(ValueError):
            await file_manager.create_file("/test/invalid.txt", "string instead of bytes")

    @pytest.mark.asyncio
    async def test_create_directory(self, file_manager, mock_backend):
        """Test creating a directory."""
        # Create a sample directory result
        dir_file = File(name="new_dir", path="/test/new_dir", type=FileType.directory)
        mock_backend.create_directory.return_value = dir_file
        
        # Test creating a directory
        result = await file_manager.create_directory("/test/new_dir")
        mock_backend.create_directory.assert_called_once_with("/test/new_dir")
        assert result == dir_file

    @pytest.mark.asyncio
    async def test_delete(self, file_manager, mock_backend):
        """Test deleting a file or directory."""
        # Test deleting a file
        await file_manager.delete("/test/file.txt")
        mock_backend.delete.assert_called_once_with("/test/file.txt", False)
        
        # Test deleting a directory recursively
        mock_backend.delete.reset_mock()
        await file_manager.delete("/test/dir", recursive=True)
        mock_backend.delete.assert_called_once_with("/test/dir", True)

    @pytest.mark.asyncio
    async def test_move_same_backend(self, file_manager, mock_backend, sample_file):
        """Test moving a file within the same backend."""
        # Set up the mock
        mock_backend.move.return_value = sample_file
        
        # Test moving a file
        result = await file_manager.move("/test/source.txt", "/test/dest.txt")
        mock_backend.move.assert_called_once_with("/test/source.txt", "/test/dest.txt")
        assert result == sample_file

    @pytest.mark.asyncio
    async def test_move_different_backends(self, mock_backend, sample_file, sample_content):
        """Test moving a file between different backends."""
        # Create another mock backend for destination
        mock_dst_backend = MagicMock(spec=StorageBackend)
        mock_dst_backend.create_file = AsyncMock(return_value=sample_file)
        
        # Set up the source backend to return content
        mock_backend.view = AsyncMock(return_value=sample_content)
        mock_backend.delete = AsyncMock()
        
        # Create file manager with two backends
        manager = FileManager()
        manager.register_backend("source_backend", mock_backend)
        manager.register_backend("dest_backend", mock_dst_backend)
        
        # Test moving between backends
        result = await manager.move(
            "/test/source.txt", "/test/dest.txt",
            src_backend="source_backend", dst_backend="dest_backend"
        )
        
        # Verify correct methods were called
        mock_backend.view.assert_called_once_with("/test/source.txt")
        mock_dst_backend.create_file.assert_called_once_with("/test/dest.txt", sample_content.content)
        mock_backend.delete.assert_called_once_with("/test/source.txt")
        assert result == sample_file

    @pytest.mark.asyncio
    async def test_copy_same_backend(self, file_manager, mock_backend, sample_file):
        """Test copying a file within the same backend."""
        # Set up the mock
        mock_backend.copy.return_value = sample_file
        
        # Test copying a file
        result = await file_manager.copy("/test/source.txt", "/test/dest.txt")
        mock_backend.copy.assert_called_once_with("/test/source.txt", "/test/dest.txt")
        assert result == sample_file

    @pytest.mark.asyncio
    async def test_copy_different_backends(self, mock_backend, sample_file, sample_content):
        """Test copying a file between different backends."""
        # Create another mock backend for destination
        mock_dst_backend = MagicMock(spec=StorageBackend)
        mock_dst_backend.create_file = AsyncMock(return_value=sample_file)
        
        # Set up the source backend to return content
        mock_backend.view = AsyncMock(return_value=sample_content)
        
        # Create file manager with two backends
        manager = FileManager()
        manager.register_backend("source_backend", mock_backend)
        manager.register_backend("dest_backend", mock_dst_backend)
        
        # Test copying between backends
        result = await manager.copy(
            "/test/source.txt", "/test/dest.txt",
            src_backend="source_backend", dst_backend="dest_backend"
        )
        
        # Verify correct methods were called
        mock_backend.view.assert_called_once_with("/test/source.txt")
        mock_dst_backend.create_file.assert_called_once_with("/test/dest.txt", sample_content.content)
        assert result == sample_file
