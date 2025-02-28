"""
Main module for the FastAPI application. This module is responsible for creating the FastAPI application, 
adding the CORS middleware, and adding the lifespan context manager to the FastAPI application. 
The lifespan context manager is used to initialize the database, add the event listener to the scheduler, 
start the scheduler, load the scheduled tasks, and create the jobs for the scheduled tasks. 
The module also imports the redirect_to_endpoints function from the routers.directory module and calls 
it to add the routers to the FastAPI application.
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import FRONTEND_API_URL
from databases.axion.init_db import initialize_database
from routers.directory import redirect_to_endpoints

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_API_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app.router.lifespan_context = lifespan
    
redirect_to_endpoints(app=app)
