"""
Team: MSG - AXIANS

Module that contains endpoints for authentication.

This module includes the setup for endpoints for authentication. It includes
routers for getting, creating, updating, and deleting users.
"""
import json
import traceback
from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import (APIRouter, Depends, HTTPException, Path, Query, Request,
                     status)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from databases.axion.handlers.primaries.LocalUser import \
    LocalUser as LocalUserHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.LocalUser import \
    LocalUser as LocalUserSchema
from databases.axion.schemas.primaries.LocalUser import RequestLocalUser
from modules.login.schemas import Token, TokenData
from modules.login.utils import create_access_token, verify_password

from ..shared.CustomLogger import CustomLogger

logger = CustomLogger('operation/login')

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 200

@router.post("", response_model=Token)
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session)
) -> Token:
    """
    Authenticate a user and return an access token.

    Args:
        request (Request): The incoming request object.
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
        db (Session): Database session dependency.

    Returns:
        Token: Token object containing access token and token type.
    """
    try:
        client_ip = request.client.host
        username = form_data.username
        password = form_data.password
        check_ldap = True

        logger.info(f"[login] Attempting to log in user with username: {username} from IP: {client_ip}")

        user = LocalUserHandler().get_local_user_by_username(db, username)
        if user is None:
            logger.info(f"[login] User {username} not found")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not verify_password(password, user.password_hash):
            logger.info(f"[login] Incorrect password for user: {username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        
        logger.info(f"[login] User {username} successfully logged in from IP: {client_ip}")

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException as httpe:
        raise httpe
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"{username} - [login] An unexpected error occurred: {repr(e)} traceback: {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
