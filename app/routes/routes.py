from fastapi import APIRouter

from app.routes import version_routes

all_api_routes = APIRouter()

all_api_routes.include_router(version_routes.router, tags=["version"])
