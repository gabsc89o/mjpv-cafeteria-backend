"""
Team: MSG - AXIANS

Module that redirects requests to the corresponding endpoints.

This module includes the setup for redirecting requests to the appropriate 
endpoints within the FastAPI application. It includes the setup for the
administration and operation endpoints.
"""

from fastapi import FastAPI

from endpoints.administration.primaries import (cierrecaja, detallefactura,
                                                factura, local_user, producto)
from endpoints.operation import login
from endpoints.shared.CustomLogger import CustomLogger

logger = CustomLogger('routers/directory')

def redirect_to_endpoints(app:FastAPI):
    """
    Registers routers with the FastAPI app for various endpoints.

    Args:
        app (FastAPI): The FastAPI application instance to which routers are added.
    """
    app.include_router(login.router,
                    prefix="/login",
                    tags=["Login"])
    app.include_router(producto.router,
                    prefix="/administration",
                    tags=["Productos"])
    app.include_router(local_user.router,
                    prefix="/administration",
                    tags=["Local Users"])
    app.include_router(factura.router,
                    prefix="/administration",
                    tags=["Facturas"])
    app.include_router(detallefactura.router,
                    prefix="/administration",
                    tags=["Detalle Facturas"])
    app.include_router(cierrecaja.router,
                    prefix="/administration",
                    tags=["Cierre Cajas"])


