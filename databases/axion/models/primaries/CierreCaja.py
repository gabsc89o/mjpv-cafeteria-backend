"""
Team: MSG - AXIANS

Module that contains models for client management.
"""
from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship

from databases.axion.init_db import Base


class CierreCaja(Base):
    __tablename__ = 'cierres_caja'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    total_ventas = Column(Float)
    is_closed = Column(Boolean)
    id_factura_inicial = Column(Integer)
    factura = relationship("Factura", back_populates="cierre_caja")
