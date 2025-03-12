from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CierreCajaSchema(BaseModel):
    id: int
    fecha: datetime
    total_ventas: float

    class Config:
        orm_mode = True

class RequestCierreCaja(BaseModel):
    fecha: datetime
    factura_id: List[int] = []
