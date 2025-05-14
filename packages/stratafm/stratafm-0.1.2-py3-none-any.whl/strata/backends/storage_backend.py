from abc import ABC, abstractmethod

from strata.entities import Content, File


class StorageBackend(ABC):
    @abstractmethod
    async def list(self, path: str, depth: int = 1) -> list[File]:
        raise NotImplementedError("list method not implemented")

    @abstractmethod
    async def view(self, path: str) -> Content:
        raise NotImplementedError("view method not implemented")

    @abstractmethod
    async def create_file(self, path: str, content: bytes) -> File:
        raise NotImplementedError("create_file method not implemented")

    @abstractmethod
    async def create_directory(self, path: str) -> File:
        raise NotImplementedError("create_directory method not implemented")

    @abstractmethod
    async def delete(self, path: str, recursive: bool = False) -> None:
        raise NotImplementedError("delete method not implemented")

    @abstractmethod
    async def move(self, src_path: str, dst_path: str) -> File:
        raise NotImplementedError("move method not implemented")

    @abstractmethod
    async def copy(self, src_path: str, dst_path: str) -> File:
        raise NotImplementedError("copy method not implemented")
