"""
Set of routes to create embeddings for files and folders.
"""

import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from temporalio.client import Client

from jobs.workflows import EmbedFilesWorkflow
from services.files import FileHandler
from utils.config import get_config
from utils.types import (
    EmbeddingFileWorkflowRequest,
    EmbeddingResponse,
)

router = APIRouter(
    prefix="/embed",
    tags=["embeddings"],
)


@router.post("/file")
async def create_embeddings_file(file: UploadFile = File(...)) -> EmbeddingResponse:
    """
    Create embeddings from an uploaded file.

    Args:
        file (UploadFile): The file to process
        metadata (Optional[dict]): Additional metadata for the document

    Returns:
        EmbeddingResponse: The embedding results
    """
    # Read file content
    content = await file.read()

    # Save the file to the ./data/files directory
    file_path = Path(f"./data/files/{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    # Upload file to Minio
    file_handler = FileHandler()
    blob_path = file_handler.upload_to_blob(file_path)

    # Create client connected to server at the given address
    temporal_client = await Client.connect(get_config().temporal_host)

    # Create workflow
    await temporal_client.start_workflow(
        EmbedFilesWorkflow.run,
        EmbeddingFileWorkflowRequest(blob_path=blob_path),
        id=f"embeddings-file-{uuid.uuid4()}",
        task_queue=get_config().temporal_queue,
    )

    return EmbeddingResponse(
        status="success",
        message="Embeddings created successfully",
    )
