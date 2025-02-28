"""
Team: MSG - AXIANS

Module that contains models for local user management.
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from databases.axion.init_db import Base


class LocalUser(Base):
    """
    Class that represents a local user in the database.
    """
    __tablename__ = "local_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
