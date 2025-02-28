from ..shared.database import Database

DATABASE_URL = "sqlite:///./mjpvcdb.db"

db = Database(database_url=DATABASE_URL)

Base = db.get_base()

def initialize_database():
    """
    Initialize the database.
 
    This function is responsible for initializing the database by creating all the necessary tables if they do not already exist.
    """
    import databases.axion.models.primaries

    # Base.metadata.drop_all(bind=db.get_engine()) # Delete all tables if they exist
    Base.metadata.create_all(bind=db.get_engine()) # Create tables if they do not exist

def get_session():
    """
    Get the database session.
    """
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()