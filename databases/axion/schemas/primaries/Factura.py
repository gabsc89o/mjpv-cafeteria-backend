from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DetalleFacturaSchema(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    precio_final: float

    class Config:
        orm_mode = True

class FacturaSchema(BaseModel):
    id: int
    fecha: datetime
    total: float

    class Config:
        orm_mode = True

class RequestDetalleFactura(BaseModel):
    producto_id: int
    cantidad: int

class RequestFactura(BaseModel):
    fecha: datetime
    detalle_ids: List[int] = []