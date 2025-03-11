from databases.axion.handlers.primaries.CierreCaja import \
    CierreCaja as ItemHandler
from databases.axion.handlers.primaries.Factura import \
    Factura as FacturaHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.CierreCaja import \
    CierreCajaSchema as ItemSchema
from databases.axion.schemas.primaries.CierreCaja import RequestCierreCaja

from ...shared.imports import *

logger = CustomLogger("administration/cierrecaja")

router = APIRouter()

@router.post("/cierre-caja", response_model=ItemSchema)
async def create_cierre_caja(cierre_caja: RequestCierreCaja, db: Session = Depends(get_session)):
    try:
        _cierre_caja = ItemHandler().create_cierre_caja(db, cierre_caja)
        return _cierre_caja
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@router.get("/cierres-caja", response_model=List[ItemSchema])
async def get_all_cierres_cajas(db: Session = Depends(get_session)):
    try:
        _items = ItemHandler().get_cierres_caja(db)
        if not _items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
        return _items
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@router.get("/cierre-caja/{id}")
async def get_cierre_caja_by_id(id: int, db: Session = Depends(get_session)):
    try:
        _item = ItemHandler().get_cierre_caja_by_id(db, id)
        if not _item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
        _facturas = FacturaHandler().get_factura_by_cierre_caja_id(db, id)
        _item.factuta_ids = [_factura.id for _factura in _facturas]
        _item.facturas = _facturas
        return _item
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)