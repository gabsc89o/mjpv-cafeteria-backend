import os
import shutil
import traceback
from typing import Annotated, List

from fastapi import (APIRouter, Body, Depends, File, HTTPException, Path,
                     Query, UploadFile, status)
from PIL import Image
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from databases.shared.database import DatabaseException
from modules.login.utils import get_current_user

from .CustomLogger import CustomLogger
