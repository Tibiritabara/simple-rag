from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.router import router
from utils.config import get_config

app = FastAPI(
    title=get_config().app_name,
    description="API for creating embeddings from files and folders",
    version=get_config().version,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_config().frontend_host],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)
