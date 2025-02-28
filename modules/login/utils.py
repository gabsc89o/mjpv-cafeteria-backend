"""
Team: MSG - AXIANS

Module that contains endpoints for authentication.

This module includes the setup for endpoints for authentication. It includes
routers for getting, creating, updating, and deleting users.
"""
import ssl
import subprocess
import traceback
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ldap3 import Connection, Server, Tls
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import ALGORITHM, SECRET_KEY
from databases.axion.handlers.primaries.LocalUser import \
    LocalUser as LocalUserHandler
from databases.axion.init_db import get_session
from databases.axion.schemas.primaries.LocalUser import \
    LocalUser as LocalUserSchema
from endpoints.shared.CustomLogger import CustomLogger

from .schemas import Token, TokenData

logger = CustomLogger('modules/authentication/utils')

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict,
                        expires_delta: timedelta | None = None):
    """
    Function to create an access token.

    Args:

        data (dict): Data to be encoded in the token.

        expires_delta (timedelta | None): Expiration time for the token.

    Returns:

        str: Encoded access token.
    """
    _to_encode = data.copy()
    if expires_delta:
        _expire = datetime.now(timezone.utc) + expires_delta
    else:
        _expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    _to_encode.update({"exp": _expire})
    _encoded_jwt = jwt.encode(_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return _encoded_jwt
        
def hash_password(password: str) -> str:
    """
    Hash a password using the bcrypt algorithm.

    :param password: The password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_session)) -> LocalUserSchema:
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token for authentication.
        db (Session): The database session.

    Returns:
        LocalUserSchema: The user object corresponding to the authenticated token.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None or not username:
            raise credentials_exception

        token_data = TokenData(username=username)

        _user = LocalUserHandler().get_local_user_by_username(db, username=token_data.username)
        if _user is None:
            raise credentials_exception
        
        return _user

    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception

    except HTTPException as httpe:
        raise httpe

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"[get_current_user] Exception occurred: {repr(e)} traceback: {repr(tb)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain-text password matches a hashed password.

    :param plain_password: The plain-text password to verify.
    :param hashed_password: The hashed password to compare.
    :return: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
