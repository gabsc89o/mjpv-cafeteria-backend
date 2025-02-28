from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class Producto(BaseModel):
    """
    Schema that represents an instance in the database.
    """
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    imagen_url: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )

    @classmethod
    def from_orm(cls, obj):
        # Deprecated, use model_validate instead
        return cls.model_validate(obj)

class RequestProducto(BaseModel):
    """
    Schema that represents an instance request in the API.
    """
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    imagen_url: Optional[str] = None
