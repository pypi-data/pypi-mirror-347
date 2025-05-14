from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    """Representa un proyecto de archivos.
    
    Un proyecto contiene la configuración necesaria para acceder a los archivos,
    incluyendo parámetros como URL base, credenciales, etc.
    """
    id: str = Field(
        ...,
        json_schema_extra={
            "description": "Identificador único del proyecto.",
            "example": "proj1",
        },
    )
    
    name: str = Field(
        ...,
        json_schema_extra={
            "description": "Nombre del proyecto.",
            "example": "Proyecto 1",
        },
    )
    
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={
            "description": "Parámetros adicionales del proyecto.",
            "example": {"base_url": "http://example.com"},
        },
    )
