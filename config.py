import configparser
import os
import traceback

from dotenv import load_dotenv

"""
Read and Load .env file
"""
load_dotenv(".env")

DB_AXION_HOSTNAME = os.getenv("DB_AXION_HOSTNAME")
DB_AXION_USER = os.getenv("DB_AXION_USER")
DB_AXION_PWD = os.getenv("DB_AXION_PWD")
DB_AXION_PORT = os.getenv("DB_AXION_PORT")
DB_AXION_DATABASE = os.getenv("DB_AXION_DATABASE")
DB_AXION_DRIVERNAME = os.getenv("DB_AXION_DRIVERNAME")

FRONTEND_API_URL = os.getenv("FRONTEND_API_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
