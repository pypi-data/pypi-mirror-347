from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class FileType(str, Enum):
    file = "file"
    directory = "directory"


class File(BaseModel):
    name: str = Field(
        ...,
        json_schema_extra={
            "description": "File name.",
            "example": "example.txt",
        },
    )

    path: str = Field(
        ...,
        json_schema_extra={
            "description": "File path.",
            "example": "/path/to/example.txt",
        },
    )

    type: FileType = Field(
        ...,
        json_schema_extra={
            "description": "File type (file or directory).",
            "example": "file",
        },
    )

    size: int | None = Field(
        None,
        json_schema_extra={
            "description": "File size in bytes.",
            "example": 1024,
        },
    )

    modified: datetime | None = Field(
        None,
        json_schema_extra={
            "description": "Last modified date.",
            "example": "2023-10-01T12:00:00Z",
        },
    )

    children: list["File"] | None = Field(
        None,
        json_schema_extra={
            "description": "List of child files (if directory).",
            "example": [
                {
                    "name": "child.txt",
                    "path": "/path/to/child.txt",
                    "type": "file",
                    "size": 512,
                    "modified": "2023-10-01T12:00:00Z",
                }
            ],
        },
    )
