from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CierreCajaSchema(BaseModel):
    id: int
    fecha: datetime
    total_ventas: float
    is_closed: bool
    id_factura_inicial: int

    model_config = ConfigDict(
        from_attributes=True
    )

    @classmethod
    def from_orm(cls, obj):
        # Deprecated, use model_validate instead
        return cls.model_validate(obj)

class RequestCierreCaja(BaseModel):
    fecha: datetime
    is_closed: bool
