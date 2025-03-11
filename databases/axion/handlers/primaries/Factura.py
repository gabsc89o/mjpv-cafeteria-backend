from sqlalchemy.orm import Session

from databases.axion.handlers.primaries.DetalleFactura import DetalleFactura
from databases.axion.models.primaries.Factura import Factura as FacturaModel
from databases.axion.schemas.primaries.Factura import (FacturaSchema,
                                                       RequestFactura)
from databases.shared.database import DatabaseException


class Factura:

    def create_factura(self, db: Session, factura: RequestFactura):
        try:
            _details_sum = 0
            for detalle_id in factura.detalle_ids:
                _detalle = DetalleFactura().get_detalle_factura_by_id(db, detalle_id)
                if _detalle is None:
                    raise DatabaseException(f"DetalleFactura with id {detalle_id} not found")
                _details_sum += _detalle.precio_final
            _factura = FacturaModel(
                fecha=factura.fecha,
                total=_details_sum,
            )
            db.add(_factura)
            db.commit()
            db.refresh(_factura)

        # Actualizar la relación de detalles
            for detalle_id in factura.detalle_ids:
                _detalle = DetalleFactura().get_detalle_factura_by_id(db, detalle_id)
                _detalle.factura_id = _factura.id
                db.commit()
                db.refresh(_detalle)
            return _factura
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_factura] An error occurred while creating the factura: {str(e)}") from e
        
    def get_facturas(self, db: Session):
        try:
            return db.query(FacturaModel).all()
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[get_facturas] An error occurred while getting the facturas: {str(e)}") from e
    
    def get_factura_by_id(self, db: Session, id: int):
        try:
            return db.query(FacturaModel).filter_by(id=id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_factura_by_id] An error occurred while getting the factura by ID: {str(e)}") from e
        
    def get_factura_by_cierre_caja_id(self, db: Session, cierre_caja_id: int):
        try:
            return db.query(FacturaModel).filter_by(cierre_caja_id=cierre_caja_id).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_factura_by_cierre_caja_id] An error occurred while getting the factura by cierre caja ID: {str(e)}") from e