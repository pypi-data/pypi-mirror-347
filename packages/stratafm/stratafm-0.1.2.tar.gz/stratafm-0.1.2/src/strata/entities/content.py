from pydantic import BaseModel, Field
from typing import Optional

class Content(BaseModel):
    file: str = Field(
        default="untitled",
        json_schema_extra={
            "description": "Filename",
            "example": "example.txt",
        }
    )
    
    content: bytes = Field(
        ...,
        json_schema_extra={
            "description": "File content",
            "example": "content of the file",  # Cambiado de bytes a str para JSON
        },
    )
    
    content_type: Optional[str] = Field(
        "application/octet-stream",
        json_schema_extra={
            "description": "Content MIME type",
            "example": "text/plain",
        },
    )
