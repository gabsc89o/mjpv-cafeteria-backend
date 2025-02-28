"""
Team: MSG - AXIANS

Module that contains models for client management.
"""
from sqlalchemy import (Column, Enum, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from databases.axion.init_db import Base


class Producto(Base):
    """
    Class that represents an instance in the database.
    """
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    imagen_url = Column(String)