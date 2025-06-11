from sqlalchemy.orm import Session

from databases.axion.handlers.primaries.Factura import \
    Factura as FacturaHandler
from databases.axion.models.primaries.CierreCaja import \
    CierreCaja as CierreCajaModel
from databases.axion.models.primaries.Factura import Factura as FacturaModel
from databases.axion.schemas.primaries.CierreCaja import (CierreCajaSchema,
                                                          RequestCierreCaja)
from databases.shared.database import DatabaseException


class CierreCaja:
    def create_cierre_caja(self, db: Session, cierre_caja: RequestCierreCaja):
        try:
            _factura_sum = 0
            last_cierre_caja = db.query(CierreCajaModel).order_by(
                CierreCajaModel.id.desc()).first()
            if last_cierre_caja:
                if last_cierre_caja.is_closed:
                    raise DatabaseException(
                        "The last cierre caja is already closed")
                last_factura = db.query(FacturaModel).order_by(
                    FacturaModel.id.desc()).first()
                if last_factura and last_cierre_caja.id_factura_inicial is not None and last_factura.id is not None:
                    all_factura = db.query(FacturaModel).filter(
                        FacturaModel.id >= last_cierre_caja.id_factura_inicial,
                        FacturaModel.id <= last_factura.id
                    ).all()
                else:
                    all_factura = []
            for factura in all_factura:
                _factura_sum += factura.total
            _factura_sum = round(_factura_sum, 2)

            if cierre_caja.is_closed:
                #Actualizar el cierre de caja
                last_cierre_caja.is_closed = cierre_caja.is_closed
                last_cierre_caja.fecha = cierre_caja.fecha
                last_cierre_caja.total_ventas = _factura_sum
                db.commit()
                db.refresh(last_cierre_caja)

                for factura in all_factura:
                    _factura = FacturaHandler().get_factura_by_id(db, factura.id)
                    _factura.cierre_caja_id = last_cierre_caja.id
                    db.commit()
                    db.refresh(_factura)
            else:
                last_cierre_caja.fecha = cierre_caja.fecha
                last_cierre_caja.total_ventas = _factura_sum
            return last_cierre_caja
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_cierre_caja] An error occurred while creating the cierre caja: {str(e)}") from e
        
    def get_cierres_caja(self, db: Session):
        try:
            cierre_caja = db.query(CierreCajaModel).all()
            if not cierre_caja:
                raise DatabaseException("No cierres caja found")
            return cierre_caja
        except Exception as e:
            raise DatabaseException(
                f"[get_cierres_caja] An error occurred while getting the cierres caja: {str(e)}") from e
        
    def get_cierre_caja_by_id(self, db: Session, id: int):
        try:
            return db.query(CierreCajaModel).filter(CierreCajaModel.id == id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_cierre_caja_by_id] An error occurred while getting the cierre caja by id: {str(e)}") from e