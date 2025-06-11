from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DetalleFacturaSchema(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    precio_final: float

    model_config = ConfigDict(
        from_attributes=True
    )

    @classmethod
    def from_orm(cls, obj):
        # Deprecated, use model_validate instead
        return cls.model_validate(obj)

class FacturaSchema(BaseModel):
    id: int
    fecha: datetime
    total: float

    model_config = ConfigDict(
        from_attributes=True
    )

    @classmethod
    def from_orm(cls, obj):
        # Deprecated, use model_validate instead
        return cls.model_validate(obj)

class RequestDetalleFactura(BaseModel):
    producto_id: int
    cantidad: int

class RequestFactura(BaseModel):
    fecha: datetime
    detalle_ids: List[int] = []