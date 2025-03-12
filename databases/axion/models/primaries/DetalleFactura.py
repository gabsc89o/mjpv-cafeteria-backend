"""
Team: MSG - AXIANS

Module that contains models for client management.
"""
from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String, UniqueConstraint)
from sqlalchemy.orm import relationship

from databases.axion.init_db import Base


class DetalleFactura(Base):
    __tablename__ = 'detalles_facturas'
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    precio_final = Column(Float)
    factura_id = Column(Integer, ForeignKey('facturas.id'))
    factura = relationship("Factura", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")