from databases.axion.handlers.primaries.DetalleFactura import \
    DetalleFactura as ItemHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.Factura import \
    DetalleFacturaSchema as ItemSchema
from databases.axion.schemas.primaries.Factura import RequestDetalleFactura
from databases.shared.database import DatabaseException

from ...shared.imports import *

logger = CustomLogger("administration/detallefactura")

router = APIRouter()


@router.get("/detallefacturas", response_model=List[ItemSchema])
async def get_all_items(db: Session = Depends(get_session)):
    try:
        _items = ItemHandler().get_detalles_facturas(db)
        if not _items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
        return _items
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/detallefactura", response_model=ItemSchema)
async def create_detalle_factura(detalle_factura: RequestDetalleFactura, db: Session = Depends(get_session)):
    try:
        _detalle_factura = ItemHandler().create_detalle_factura(db, detalle_factura)
        return _detalle_factura
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))