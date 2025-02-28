"""
Team: MSG - AXIANS

Module that contains handlers for local user management.
"""
from sqlalchemy.orm import Session

from databases.axion.models.primaries.LocalUser import \
    LocalUser as LocalUserModel
from databases.axion.schemas.primaries.LocalUser import \
    LocalUser as LocalUserSchema
from databases.axion.schemas.primaries.LocalUser import RequestLocalUser
from databases.shared.database import DatabaseException


class LocalUser:
    """
    Class that contains methods for local user management.
    """

    def create_local_user(self, db: Session, local_user: RequestLocalUser):
        """
        Create a new local user.

        Args:
            db (Session): The database session.
            local_user (LocalUserSchema): The local user data.

        Returns:
            LocalUser: The local user object
        """
        _local_user = LocalUserModel(username=local_user.username, password_hash=local_user.password)
        
        try:
            db.add(_local_user)
            db.commit()
            db.refresh(_local_user)
            return _local_user
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[create_local_user] An error occurred while updating the local user: {str(e)}") from e

    def get_all_local_users(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get all local users.

        Args:

            db (Session): The database session.
            skip (int, optional): The number of local users to skip. Defaults to 0.
            limit (int, optional): The maximum number of local users to return. Defaults to 100.

        Returns:

            list: A list of all local users.
        """
        try:
            return db.query(LocalUserModel).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseException(
                f"[get_all_local_users] An error occurred while get all local users: {str(e)}") from e


    def get_local_user_by_id(self, db: Session, id: int):
        """
        Get a local user by ID.

        Args:

            db (Session): The database session.
            id (int): The ID of the local user.

        Returns:

            LocalUser: The local user object.
        """
        try:
            return db.query(LocalUserModel).filter_by(id=id).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_local_user_by_id] An error occurred while get local user by ID: {str(e)}") from e



    def get_local_user_by_username(self, db: Session, username: str):
        """
        Get a local user by username.

        Args:

            db (Session): The database session.
            username (str): The username of the local user.

        Returns:

            LocalUser: The local user object.
        """
        try:
            return db.query(LocalUserModel).filter_by(username=username).first()
        except Exception as e:
            raise DatabaseException(
                f"[get_local_user_by_username] An error occurred while get local user by username: {str(e)}") from e

    def remove_local_user(self, db: Session, id: int):
        """
        Remove a local user by ID.

        Args:

            db (Session): The database session.
            id (int): The ID of the local user.

        Returns:

            LocalUser: The local user object.
        """
        try:
            _local_user = db.query(LocalUserModel).filter_by(id=id).first()
            db.delete(_local_user)
            db.commit()
            return _local_user
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[remove_local_user] An error occurred while removing the local user: {str(e)}") from e


    def update_local_user(self,
                    db: Session,
                    id: int,
                    username: str,
                    password_hash: str):
        """
        Update a local user by ID.

        Args:

            db (Session): The database session.
            id (int): The ID of the local user.
            username (str): The new username.
            password_hash (str): The new password hash.

        Returns:

            LocalUser: The updated local user object.

        """
        try:
            _local_user = db.query(LocalUserModel).filter_by(id=id).first()
            _local_user.username = username
            _local_user.password_hash = password_hash
            db.commit()
            db.refresh(_local_user)
            return _local_user
        except Exception as e:
            db.rollback()
            raise DatabaseException(
                f"[update_local_user] An error occurred while updating the local user: {str(e)}") from e


    def __str__(self):
        """
        Return a JSON string representation of the user with indentation.
        """
        try:
            return self.model_dump_json(indent=3)
        except Exception as e:
            return f"[__str__] Error displaying user: {str(e)}"
