"""
Set of routes for the v1 API.
"""

from fastapi import APIRouter

from routes.v1.embeddings import router as embeddings_router
from routes.v1.query import router as query_router

router = APIRouter(prefix="/v1")

router.include_router(embeddings_router)
router.include_router(query_router)
