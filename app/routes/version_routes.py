from typing import Any
from fastapi import APIRouter
from app.routes import generic_constants

router = APIRouter()


@router.get("/api/version")
async def get_version() -> Any:
    """
    Get Application Version.
    """
    VERSION = generic_constants.APP_VERSION
    return {"version": VERSION}
