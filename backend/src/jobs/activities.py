"""
Set of temporal activities to execute asynchronously.
"""

from pathlib import Path

from temporalio import activity

from services.embeddings import VectorStoreHandler
from services.files import FileHandler, TextExtractor
from utils.config import get_config
from utils.types import EmbeddingFileWorkflowRequest, EmbeddingResponse


@activity.defn
def embed_file(request: EmbeddingFileWorkflowRequest) -> EmbeddingResponse:
    """
    Embed a file.

    Args:
        request (EmbeddingFileRequest): The request to embed a file.

    Returns:
        (EmbeddingResponse): The response from the activity.
    """
    blob_path = request.blob_path

    # Download the file from the blob storage
    file_path = Path(f"./data/tmp/{blob_path}")
    file_handler = FileHandler()
    file_handler.download_from_blob(
        get_config().storage_bucket,
        blob_path,
        str(file_path),
    )

    # Extract the text from the file
    text_extractor = TextExtractor()
    documents = text_extractor.extract_text_from_file(file_path)

    # Create embeddings for the documents
    vector_store = VectorStoreHandler()
    vector_store.from_documents(documents)

    return EmbeddingResponse(
        status="success",
        message="Embeddings created successfully",
        details={
            "blob_path": blob_path,
            "documents": len(documents),
        },
    )
