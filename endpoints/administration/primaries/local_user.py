"""
Team: MSG - AXIANS

Module that contains endpoints for local user management.

This module includes the setup for endpoints for local user management. It includes
routers for getting, creating, updating, and deleting local users.
"""

from databases.axion.handlers.primaries.LocalUser import \
    LocalUser as LocalUserHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.LocalUser import \
    LocalUser as LocalUserSchema
from databases.axion.schemas.primaries.LocalUser import RequestLocalUser
from modules.login.utils import hash_password

from ...shared.imports import *

logger = CustomLogger("administration/local_users")

router = APIRouter()


@router.get("/local-users", 
            response_model=List[LocalUserSchema],
            status_code=status.HTTP_200_OK,
            summary="Get all local users of Axion.",
            response_description="All local users of Axion.")
async def get_all_local_users(
    current_user: Annotated[LocalUserSchema, Depends(get_current_user)],
    db: Session = Depends(get_session)) -> List[LocalUserSchema]:
    """
    Get all local users.
    
    This function retrieves all local user data from the database.
    
    Args:
        db (Session): The database session.

    Returns:
        List[LocalUserSchema]: A list of all local user data.
    
    Raises:
        HTTPException: If no local users are found or if there is an internal server error.
    """
    try:
        logger.info(f"{current_user.username} - [get_all_local_users] Getting all local users.")
        _local_users = LocalUserHandler().get_all_local_users(db)
        
        if not _local_users:
            logger.info(f"{current_user.username} - [get_all_local_users] No local users found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No local users found.")
        
        logger.info(f"{current_user.username} - [get_all_local_users] localUsers found.")
        return _local_users
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} - [get_all_local_users] Exception occurred: {repr(e)} traceback: {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch all local users.") from e

@router.post("/local-user", 
            response_model=LocalUserSchema,
            response_model_include=["username", "id"],
            responses={
                201: {
                    "content": {
                        "application/json": {
                            "example":{ "id": 1,"username": "my_username"}
                        }
                    },
                },
            },
            status_code=status.HTTP_201_CREATED,
            summary="Add a new local user of Axion.",
            response_description="The newly created local user data.")
async def add_new_local_user(
    request: RequestLocalUser,
    db: Session = Depends(get_session))-> LocalUserSchema:
    """
    Add a new local user.

    This function is used to add a new local user to the system. It takes the current authenticated local user,
    the request with local user data, and the database session as parameters.

    Args:
        request (RequestLocalUser): The request with local user data.
        db (Session): The database session.

    Returns:
        LocalUserSchema: The newly created local user data.

    Raises:
        HTTPException: If the local user is not authenticated, or if the local user already exists, or if there is an internal server error.
    """
    try:
        logger.info(f"[add_new_local_user] Adding new local user {request.username}.")
        existing_user = LocalUserHandler().get_local_user_by_username(db, request.username)

        if existing_user is not None:
            logger.info(f"[add_new_local_user] Local User {request.username} already exists.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Local User already exists.") 
       
        request.password = hash_password(request.password)
        
        _new_local_user = LocalUserHandler().create_local_user(db, request)
        
        if _new_local_user is None:
            tb = traceback.format_exc()
            logger.error(f"[add_new_local_user] New local user is None: {repr(e)} traceback {repr(tb)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Could not create local user due to an internal error.")
        logger.info(f"[add_new_local_user] Local User {request.username} added.")
        return _new_local_user
        
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"[add_new_local_user] Exception general occurred: {repr(e)} traceback {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add new local user") from e

@router.put("/local-user", 
            response_model=LocalUserSchema,
            response_model_include=["username", "id"],
            responses={
                200: {
                    "content": {
                        "application/json": {
                            "example":{ "id": 1,"username": "my_username"}
                        }
                    },
                },
            },
            status_code=status.HTTP_200_OK,
            summary="Update a local user of Axion.",
            response_description="The updated local user data.")
async def update_local_user(
    current_user: Annotated[LocalUserSchema, Depends(get_current_user)],
    request: LocalUserSchema,
    db: Session = Depends(get_session)):
    """
    Update a local user.

    This function updates the information of a local user in the database.

    Args:
        current_user (LocalUserSchema): The current local user making the request.
        request (LocalUserSchema): The updated local user information.
        db (Session): The database session.

    Returns:
        LocalUserSchema: The updated local user object.

    Raises:
        HTTPException: If the local user is not found or if there is a database error.
    """
    try:
        logger.info(f"{current_user.username} - [update_local_user] Updating local user {request.username}.")
        user = LocalUserHandler().get_local_user_by_id(db, request.id)
        if user is None:
            logger.error(f"{current_user.username} - [update_local_user] Local User {request.id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local User {request.id} not found")
        existing_user = LocalUserHandler().get_local_user_by_username(db, request.username)
        if existing_user is not None and existing_user.id != request.id:
            logger.info(f"{current_user.username} - [update_local_user] Local User {request.username} already exists.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Local User {request.username} already exists.")        
        _update_local_user = LocalUserHandler().update_local_user(db,
                                        request.id,
                                        request.username,
                                        hash_password(request.password_hash))
        logger.info(f"{current_user.username} - [update_local_user] Local User {request.username} updated.")
        return  LocalUserSchema.from_orm(_update_local_user)
    except DatabaseException as de:
        logger.error(f"{current_user.username} - [update_local_user] Database error: {de.message}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error. Failed to update local user")
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} - [update_local_user] General exception occurred: {repr(e)} traceback {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update local user") from e

@router.delete("/local-user", 
            response_model=LocalUserSchema,
            response_model_include=["id", "username"],
            responses={
                200: {
                    "content": {
                        "application/json": {
                            "example":{ "id": 1,"username": "my_username"}
                        }
                    },
                },
            },
            status_code=status.HTTP_200_OK,
            summary="Delete a local user of Axion.",
            response_description="The deleted local user data.")
async def delete_local_user(
    current_user: Annotated[LocalUserSchema, Depends(get_current_user)],
    db: Session = Depends(get_session),
    id: int = Query(ge=1,description="The ID of the local user must be an \
                                           integer greater than zero.")):
    """
    Delete one local user.
    
    Args:
        current_user (LocalUserSchema): The authenticated local user making the request.
        db (Session): The database session.
        id (int): The ID of the local user to be deleted.

    Returns:
        LocalUserSchema: The deleted local user.

    Raises:
        HTTPException: If the local user is not found or if there is a database error.
    """
    try:
        logger.info(f"{current_user.username} - [delete_local_user] Deleting local user {id}.")
        user = LocalUserHandler().get_local_user_by_id(db, id)
        if user is None:
            logger.info(f"{current_user.username} - [delete_local_user] Local User {id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local User {id} not found")
        _delete_local_user = LocalUserHandler().remove_local_user(db, id)
        logger.info(f"{current_user.username} - [delete_local_user] Local User {id} deleted.")
        return LocalUserSchema.from_orm(_delete_local_user)
    except DatabaseException as de:
        logger.error(f"{current_user.username} - [delete_local_user] Database error: {de.message}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error. Failed to delete local user")
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} - [delete_local_user] General exception occurred: {repr(e)} traceback {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete local user") from e

@router.get("/local-user-by-name/{username}",
            response_model=LocalUserSchema,
            response_model_include=["username", "id"],
            responses={
                200: {
                    "content": {
                        "application/json": {
                            "example":{ "id": 1,"username": "my_username"}
                        }
                    },
                },
            },
            status_code=status.HTTP_200_OK,
            summary = "Get an local user by username.",
            response_description = "Get an local user by username.")
async def get_local_user_by_username(
    current_user: Annotated[LocalUserSchema, Depends(get_current_user)],
    db: Session = Depends(get_session),
    username:str = Path(...,
                       description="The username/email of the local user.")) -> LocalUserSchema:
    """
    Retrieves a local user by their username.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_session).
        username (str): The username or email of the local user.

    Returns:
        LocalUserSchema: The local user object.

    Raises:
        HTTPException: If the local user is not found or an unexpected error occurs.
    """
    try:
        logger.info(f"{current_user.username} - [get_local_user_by_username] Getting local user {username}.")
        _local_user = LocalUserHandler().get_local_user_by_username(db, username)   
        if _local_user is None:
            logger.info(f"{current_user.username} - [get_local_user_by_username] Local User {username} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local User {username} not found")
        
        logger.info(f"{current_user.username} - [get_local_user_by_username] Local User {username} found.")
        return LocalUserSchema.from_orm(_local_user)
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} - [get_local_user_by_username] Exception occurred: {repr(e)} traceback {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@router.get("/local-user-by-id/{id}",
            response_model=LocalUserSchema,
            response_model_include=["id", "username"],
            responses={
                200: {
                    "content": {
                        "application/json": {
                            "example":{ "id": 1,"username": "my_username"}
                        }
                    },
                },
            },
            status_code=status.HTTP_200_OK,
            summary = "Get an local user by id.",
            response_description = "Get an local user by id.")
async def get_local_user_by_id(
    current_user: Annotated[LocalUserSchema, Depends(get_current_user)],
    db: Session = Depends(get_session),
    id:int = Path(ge=1, description="The ID of the local user must be an integer greater \
                                                than zero.")) -> LocalUserSchema:
    """
    Get a specific local user.

    This function retrieves a specific local user from the database based on the provided local user ID.

    Args:
        current_user (LocalUserSchema): The currently authenticated local user.
        db (Session): The database session.
        id (int): The ID of the local user to retrieve.

    Returns:
        LocalUserSchema: The specified local user.

    Raises:
        HTTPException: If the local user with the specified ID is not found or if an unexpected error occurs.
    """
    try:
        logger.info(f"{current_user.username} - [get_local_user_by_id] Getting local user {id}.")
        _local_user = LocalUserHandler().get_local_user_by_id(db, id)
        
        if _local_user is None:
            logger.info(f"{current_user.username} - [get_local_user_by_id] Local User id {id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Local User id {id} not found")

        logger.info(f"{current_user.username} - [get_local_user_by_id] Local User {id} found.")
        return LocalUserSchema.from_orm(_local_user)
    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{current_user.username} - [get_local_user_by_id] Exception occurred: {repr(e)} traceback {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred.")
