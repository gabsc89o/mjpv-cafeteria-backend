"""
Team: MSG - AXIANS

Module that contains models for client management.
"""
from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String, UniqueConstraint)
from sqlalchemy.orm import relationship

from databases.axion.init_db import Base


class Factura(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    total = Column(Float)
    cierre_caja_id = Column(Integer, ForeignKey('cierres_caja.id'))
    detalles = relationship("DetalleFactura", back_populates="factura")
    cierre_caja = relationship("CierreCaja", back_populates="factura")
