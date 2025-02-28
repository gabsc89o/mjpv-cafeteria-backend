"""
Team: MSG - AXIANS

Module that contains handlers for items management.
"""
from sqlalchemy.orm import Session

from databases.axion.models.primaries.Producto import Producto as ItemModel
from databases.axion.schemas.primaries.Producto import Producto as ItemSchema
from databases.axion.schemas.primaries.Producto import RequestProducto
from databases.shared.database import DatabaseException


class Producto:
    
    def create_item(self, db: Session, item: RequestProducto):
        """
        Create a new item.

        Args:
            db (Session): The database session.
            item (Item): The item data.

        Returns:
            Item: The created item.

        Raises:
            DatabaseException: If an error occurs while creating the item.
        """
        try:
            _item = ItemModel(nombre=item.nombre, descripcion=item.descripcion, precio=item.precio, imagen_url=item.imagen_url)
            db.add(_item)
            db.commit()
            db.refresh(_item)
            return _item
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_item] An error occurred while creating the item: {str(e)}") from e
    
    def update_item(self, db: Session, item: ItemSchema):
        """
        Update an item.

        Args:
            db (Session): The database session.
            item (Item): The item data.

        Returns:
            Item: The updated item.

        Raises:
            DatabaseException: If an error occurs while updating the item.
        """
        try:
            _item = db.query(ItemModel).filter(ItemModel.id == item.id).first()
            if not _item:
                raise DatabaseException(f"Item with id {item.id} not found")
            _item.nombre = item.nombre
            _item.descripcion = item.descripcion
            _item.precio = item.precio
            db.commit()
            db.refresh(_item)
            return _item
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[update_item] An error occurred while updating the item: {str(e)}") from e

    def update_item_image(self, db: Session, item_id: int, image_url: str) -> ItemSchema:
        """
        Update an item's image.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item.
            image_url (str): The URL of the new image.

        Returns:
            Item: The updated item with new image.

        Raises:
            DatabaseException: If an error occurs while updating the item image.
        """
        try:
            _item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
            if not _item:
                raise DatabaseException(f"Item with id {item_id} not found")

            _item.imagen_url = image_url
            db.commit()
            db.refresh(_item)
            return _item
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[update_item_image] An error occurred while updating the item image: {str(e)}") from e

    def get_all_items(self, db: Session, skip: int = 0, limit: int = 200):

        """
        Get all items.

        Args:
            db (Session): The database session.
            skip (int, optional): The number of items to skip. Defaults to 0.
            limit (int, optional): The maximum number of items to return. Defaults to 200.

        Returns:
            list: A list of all items.

        Raises:
            DatabaseException: If an error occurs while retrieving items.
        """
        try:
            return db.query(ItemModel).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_all_items] An error occurred while retrieving items: {str(e)}") from e
    
    def get_item_by_id(self, db: Session, id: int):
        """
        Get an item by id.

        Args:
            db (Session): The database session.
            id (int): The item id.

        Returns:
            Item: The item.

        Raises:
            DatabaseException: If an error occurs while retrieving the item.
        """
        try:
            return db.query(ItemModel).filter(ItemModel.id == id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_item_by_id] An error occurred while retrieving the item: {str(e)}") from e
    
    def delete_item (self, db: Session, id: int):
        """
        Delete an item.

        Args:
            db (Session): The database session.
            id (int): The item id.

        Raises:
            DatabaseException: If an error occurs while deleting the item.
        """
        try:
            _delete_item = db.query(ItemModel).filter_by(id=id).first()
            db.delete(_delete_item)
            db.commit()
            return _delete_item
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[delete_item] An error occurred while deleting the item: {str(e)}") from e
    
    def __str__(self):
        """
        Return the string representation of the class.
        """
        try:
            return self.model_dump_json(indent=3)
        except Exception as e:
            return f"[__str__] Error displaying collection: {str(e)}"
