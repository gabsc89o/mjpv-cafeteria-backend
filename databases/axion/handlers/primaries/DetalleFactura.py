from sqlalchemy.orm import Session

from databases.axion.handlers.primaries.Producto import Producto
from databases.axion.models.primaries.DetalleFactura import \
    DetalleFactura as DetalleFacturaModel
from databases.axion.schemas.primaries.Factura import (DetalleFacturaSchema,
                                                       RequestDetalleFactura)
from databases.shared.database import DatabaseException


class DetalleFactura:
    def get_detalles_facturas(self, db: Session, skip: int = 0, limit: int = 200):
        try:
            return db.query(DetalleFacturaModel).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_detalles_facturas] An error occurred while getting the detalles facturas: {str(e)}") from e

    def create_detalle_factura(self, db: Session, detalle_factura: RequestDetalleFactura):
        try:
            _producto = Producto().get_item_by_id(db, detalle_factura.producto_id)
            if _producto is None:
                raise DatabaseException(f"Producto with id {detalle_factura.producto_id} not found")
            _precio_final = _producto.precio * detalle_factura.cantidad
            _precio_final = round(_precio_final, 2)
            _detalle_factura = DetalleFacturaModel(
                producto_id=detalle_factura.producto_id,
                cantidad=detalle_factura.cantidad,
                precio_unitario=_producto.precio,
                precio_final=_precio_final
            )
            db.add(_detalle_factura)
            db.commit()
            db.refresh(_detalle_factura)
            return _detalle_factura
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_detalle_factura] An error occurred while creating the detalle factura: {str(e)}") from e

    def get_detalle_factura_by_id(self, db: Session, id: int):
        try:
            return db.query(DetalleFacturaModel).filter_by(id=id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_detalle_factura_by_id] An error occurred while get detalle factura by ID: {str(e)}") from e
        
    def get_detalle_factura_by_factura_id(self, db: Session, factura_id: int):
        try:
            return db.query(DetalleFacturaModel).filter_by(factura_id=factura_id).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_detalle_factura_by_factura_id] An error occurred while get detalle factura by factura ID: {str(e)}") from e
