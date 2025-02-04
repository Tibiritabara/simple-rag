"""
Set of types relevant for the application operations.
"""

import uuid
from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, DirectoryPath, Field, FilePath
from typing_extensions import TypedDict


class EmbeddingFileRequest(BaseModel):
    """
    Request to create embeddings for a file.

    Attributes:
        file_path(FilePath): The path to the file to create embeddings for.
    """

    file_path: FilePath


class EmbeddingFileWorkflowRequest(BaseModel):
    """
    Request to create embeddings for a file.

    Attributes:
        blob_path(str): The path to the file in the blob storage.
    """

    blob_path: str


class EmbeddingFolderRequest(BaseModel):
    """
    Request to create embeddings for a folder.

    Attributes:
        folder_path(DirectoryPath): The path to the folder to create embeddings for.
    """

    folder_path: DirectoryPath


class EmbeddingResponse(BaseModel):
    """
    Response to create embeddings.

    Attributes:
        status(str): The status of the response.
        message(str): The message of the response.
        details(dict[str, str | int | float | bool]): The details of the response.
    """

    status: str
    message: str
    details: dict[str, str | int | float | bool] = {}


class QueryRequest(BaseModel):
    """
    Request to query the embeddings.

    Attributes:
        query(str): The user query.
    """

    query: str


class Source(BaseModel):
    text: str
    metadata: dict = {}


class QueryResponse(BaseModel):
    """
    Response to query the embeddings.

    Attributes:
        message(str): The message of the response.
        sources(list[NodeWithScore]): The sources of the response.
    """

    message: str | None = None
    reasoning: str | None = None
    sources: list[Source] = []


class DocumentResponse(BaseModel):
    """
    Response containing document information.

    Attributes:
        id(uuid.UUID): The ID of the document.
        text(str): The text content of the document.
        metadata(dict): Additional metadata about the document.
    """

    id: uuid.UUID
    text: str
    metadata: dict = {}


class GetDocumentsResponse(BaseModel):
    """
    Response containing a list of documents with pagination info.

    Attributes:
        documents(list[DocumentResponse]): The list of documents.
        total_documents(int): The total number of documents available.
        page(int): The current page number.
        total_pages(int): The total number of pages available.
    """

    documents: list[DocumentResponse]
    total_documents: int


class AgenticRagState(TypedDict):
    """
    State for the agentic RAG process.

    Attributes:
        messages(Annotated[Sequence[BaseMessage], add_messages]): The messages of the conversation.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]


class DocumentGrade(BaseModel):
    """
    Binary score to validate a document relevance.

    Attributes:
        is_relevant(bool): Whether the document is relevant to the query.
    """

    is_relevant: bool = Field(
        description="Whether the document is relevant to the query.",
    )
