from sqlalchemy.orm import Session

from databases.axion.handlers.primaries.Factura import \
    Factura as FacturaHandler
from databases.axion.models.primaries.CierreCaja import \
    CierreCaja as CierreCajaModel
from databases.axion.schemas.primaries.CierreCaja import (CierreCajaSchema,
                                                          RequestCierreCaja)
from databases.shared.database import DatabaseException


class CierreCaja:
    def create_cierre_caja(self, db: Session, cierre_caja: RequestCierreCaja):
        try:
            _factura_sum = 0
            for factura_id in cierre_caja.factura_id:
                _factura = FacturaHandler().get_factura_by_id(db, factura_id)
                if _factura is None:
                    raise DatabaseException(f"Factura with id {factura_id} not found")
                _factura_sum += _factura.total
            _factura_sum = round(_factura_sum, 2)
            _cierre_caja = CierreCajaModel(
                fecha=cierre_caja.fecha,
                total_ventas=_factura_sum,
            )
            db.add(_cierre_caja)
            db.commit()
            db.refresh(_cierre_caja)

            for factura_id in cierre_caja.factura_id:
                _factura = FacturaHandler().get_factura_by_id(db, factura_id)
                _factura.cierre_caja_id = _cierre_caja.id
                db.commit()
                db.refresh(_factura)
            return _cierre_caja
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_cierre_caja] An error occurred while creating the cierre caja: {str(e)}") from e
        
    def get_cierres_caja(self, db: Session):
        try:
            return db.query(CierreCajaModel).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_cierres_caja] An error occurred while getting the cierres caja: {str(e)}") from e
        
    def get_cierre_caja_by_id(self, db: Session, id: int):
        try:
            return db.query(CierreCajaModel).filter(CierreCajaModel.id == id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_cierre_caja_by_id] An error occurred while getting the cierre caja by id: {str(e)}") from e