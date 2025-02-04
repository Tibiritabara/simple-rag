"""
Set of routes for the API.
"""

from fastapi import APIRouter

from routes.v1.v1router import router as v1_router

router = APIRouter()

router.include_router(v1_router)


@router.get("/")
async def root():
    """
    Root endpoint that returns a simple status message.

    Returns:
        dict: Status message
    """
    return {"status": "ok"}


@router.get("/health")
async def health():
    """
    Health check endpoint.

    Returns:
        dict: Status message
    """
    return {"status": "ok"}
