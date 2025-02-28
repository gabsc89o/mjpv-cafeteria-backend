"""
Team: MSG - AXIANS

Module that contains endpoints for equipment management.

This module includes the setup for endpoints for equipment management. It includes
routers for getting, creating, updating, and deleting items.
"""

from databases.axion.handlers.primaries.Producto import Producto as ItemHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.LocalUser import \
    LocalUser as LocalUserSchema
from databases.axion.schemas.primaries.Producto import Producto as ItemSchema
from databases.axion.schemas.primaries.Producto import \
    RequestProducto as RequestItemSchema
from databases.shared.database import DatabaseException

from ...shared.imports import *

logger = CustomLogger("administration/producto")

router = APIRouter()


@router.get("/productos",
            response_model=List[ItemSchema],
            status_code=status.HTTP_200_OK,
            summary="Get all items",
            response_description="A list of all items")
async def get_all_items(
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session))-> List[ItemSchema]:
    """
    Get all items.

    Args:
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.

    Returns:
        list: A list of all items.

    Raises:
        DatabaseException: If an error occurs while retrieving items.
    """
    try:
        logger.info(f"{current_user.username} [get_all_items] is getting all items")
        _items = ItemHandler().get_all_items(db)
        if not _items:      
            logger.info(f"{current_user.username} [get_all_items] no items found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
        logger.info(f"{current_user.username} [get_all_items] items found")
        return _items
    except DatabaseException as de:
        logger.error(f"{current_user.username} [get_all_items] {de}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [get_all_items] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/producto",
                response_model=ItemSchema,
                status_code=status.HTTP_201_CREATED,
                summary="Create an item",
                response_description="The created item")
async def create_item(
    item: RequestItemSchema = Depends(),
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session),
    file: UploadFile = File(...))-> ItemSchema:
    """
    Create an item.

    Args:
        item (RequestItemSchema): The item data.
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.

    Returns:
        Item: The created item.

    Raises:
        DatabaseException: If an error occurs while creating the item.
    """
    try:
        logger.info(f"{current_user.username} [create_item] is creating an item")
        # Guardar la imagen
        file_location = f"images/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        item.imagen_url = file_location  # Actualizar la URL de la imagen en el objeto item
        _item = ItemHandler().create_item(db, item)
        logger.info(f"{current_user.username} [create_item] item created")
        return _item
    except DatabaseException as de:
        logger.error(f"{current_user.username} [create_item] {de}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [create_item] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/producto",
            response_model=ItemSchema,
            status_code=status.HTTP_200_OK,
            summary="Update an item",
            response_description="The updated item")
async def update_item(
    item: ItemSchema,
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session)) -> ItemSchema:
    """
    Update an item.

    Args:
        item (RequestItemSchema): The item data.
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.

    Returns:
        Item: The updated item.

    Raises:
        DatabaseException: If an error occurs while updating the item.
    """
    try:
        logger.info(f"{current_user.username} [update_item] is updating an item")
        _item = ItemHandler().update_item(db, item)
        logger.info(f"{current_user.username} [update_item] item updated")
        return _item
    except DatabaseException as de:
        logger.error(f"{current_user.username} [update_item] {de}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [update_item] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/producto/imagen",
            response_model=ItemSchema,
            status_code=status.HTTP_200_OK,
            summary="Update an item image",
            response_description="The updated item with new image")
async def update_item_image(
    item_id: int,
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session),
    file: UploadFile = File(...)) -> ItemSchema:
    """
    Update an item image.

    Args:
        item_id (int): The ID of the item.
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.
        file (UploadFile): The image file.

    Returns:
        Item: The updated item with new image.

    Raises:
        DatabaseException: If an error occurs while updating the item image.
    """
    try:
        logger.info(f"{current_user.username} [update_item_image] is updating an item image")
        
        # Guardar la imagen
        file_location = f"images/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Actualizar la URL de la imagen en la base de datos
        _item = ItemHandler().update_item_image(db, item_id, file_location)
        logger.info(f"{current_user.username} [update_item_image] item image updated")
        return _item
    except DatabaseException as de:
        logger.error(f"{current_user.username} [update_item_image] {de}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [update_item_image] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/producto",
            response_model=ItemSchema,
            status_code=status.HTTP_200_OK,
            summary="Delete an item",
            response_description="The deleted item")
async def delete_item(
    id: int,
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session)) -> ItemSchema:
    """
    Delete an item.

    Args:
        id (int): The item id.
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.

    Returns:
        Item: The deleted item.

    Raises:
        DatabaseException: If an error occurs while deleting the item.
    """
    try:
        logger.info(f"{current_user.username} [delete_item] is deleting an item")
        _item = ItemHandler().delete_item(db, id)
        logger.info(f"{current_user.username} [delete_item] item deleted")
        return _item
    except DatabaseException as de:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [delete_item] {de}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [delete_item] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/producto-by-id/{id}",
            response_model=ItemSchema,
            status_code=status.HTTP_200_OK,
            summary="Get an item by id",
            response_description="The item found")
async def get_item_by_id(
    id: int,
    current_user: LocalUserSchema = Depends(get_current_user),
    db: Session = Depends(get_session)) -> ItemSchema:
    """
    Get an item by id.

    Args:
        id (int): The item id.
        current_user (LocalUserSchema): The current user.
        db (Session): The database session.

    Returns:
        Item: The item found.

    Raises:
        DatabaseException: If an error occurs while retrieving the item.
    """
    try:
        logger.info(f"{current_user.username} [get_item_by_id] is getting an item by id")
        _item = ItemHandler().get_item_by_id(db, id)
        if not _item:
            logger.info(f"{current_user.username} [get_item_by_id] no item found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
        logger.info(f"{current_user.username} [get_item_by_id] item found")
        return _item
    except DatabaseException as de:
        logger.error(f"{current_user.username} [get_item_by_id] {de}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(de))
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} [get_item_by_id] {str(e)}\n{tb}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
