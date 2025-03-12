from databases.axion.handlers.primaries.DetalleFactura import \
    DetalleFactura as DetalleFacturaHandler
from databases.axion.handlers.primaries.Factura import Factura as ItemHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.Factura import \
    FacturaSchema as ItemSchema
from databases.axion.schemas.primaries.Factura import RequestFactura
from databases.shared.database import DatabaseException

from ...shared.imports import *

logger = CustomLogger("administration/factura")

router = APIRouter()

@router.get("/facturas", response_model=List[ItemSchema])
async def get_all_items(db: Session = Depends(get_session)):
    try:
        _items = ItemHandler().get_facturas(db)
        if not _items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
        return _items
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)

@router.get("/factura-by-id/{id}")
async def get_item_by_id(id: int, db: Session = Depends(get_session)):
    try:
        _factura = ItemHandler().get_factura_by_id(db, id)
        if not _factura:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
        _detalles = DetalleFacturaHandler().get_detalle_factura_by_factura_id(db, id)
        _factura.detalle_ids = [_detalle.id for _detalle in _detalles]
        _factura.detalles = _detalles
        return _factura
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)

@router.post("/factura", response_model=ItemSchema)
async def create_item(item: RequestFactura, db: Session = Depends(get_session)):
    try:
        _item = ItemHandler().create_factura(db, item)
        return _item
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    