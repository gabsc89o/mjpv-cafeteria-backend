from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import ArgumentError, ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker


class Database:
    def __init__(self, database_url):
        self.database_url = database_url
        self._engine = None
        self._sessionmaker = None
        self._Base = None
        self._inspector = None
       
        self._create_engine()
        self._create_sessionmaker()
        self._create_base()
        self._create_inspector()
   
    def _create_engine(self):
        try:
            self._engine = create_engine(self.database_url, connect_args={"check_same_thread": False})
        except ArgumentError as e:
            raise ValueError(f"Error creating engine: {e}")
   
    def _create_sessionmaker(self):
        if self._engine is not None:
            self._sessionmaker = sessionmaker(bind=self._engine)
        else:
            raise ValueError("Engine is not initialized")
   
    def _create_base(self):
        self._Base = declarative_base()
   
    def _create_inspector(self):
        self._inspect = inspect(self._engine)
   
    def get_base(self):
        return self._Base
   
    def get_session(self):
        if self._sessionmaker is not None:
            return self._sessionmaker()
        else:
            raise ValueError("Sessionmaker is not initialized")
 
    def get_engine(self):
        if self._engine is not None:
            return self._engine
        else:
            raise ValueError("Engine is not initialized")
   
    def get_inspector(self):
        if self._engine is not None:
            return self._inspect
        else:
            raise ValueError("Engine is not initialized")
            
    def create_database(self, db_name):
        # SQLite does not support creating databases dynamically
        raise NotImplementedError("SQLite does not support creating databases dynamically")

class DatabaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)