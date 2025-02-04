"""
Set of routes to create embeddings for files and folders.
"""

from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from services.rag import AgenticRagService, RagService
from utils.types import (
    QueryRequest,
    QueryResponse,
)

router = APIRouter(
    prefix="/query",
    tags=["query"],
)


@router.post("/simple")
async def execute_simple_query(
    query: QueryRequest,
) -> QueryResponse:
    """
    Execute a simple query against the vector store.

    Args:
        query(QueryRequest): The query to execute.

    Returns:
        (QueryResponse): The response containing the status and message.
    """
    rag_service = RagService()
    response = rag_service.query(query.query)
    return response


@router.post("/agentic")
async def execute_agentic_query(
    query: QueryRequest,
) -> QueryResponse:
    """
    Execute a query to get the documents that match the query.

    Args:
        query(QueryRequest): The query to execute.

    Returns:
        (QueryResponse): The response containing the sources and message.
    """
    rag_service = AgenticRagService()
    graph = rag_service.generate_rag_graph()
    response = graph.invoke({"messages": [HumanMessage(content=query.query)]})
    return QueryResponse(
        message=response["messages"][-1].content,
    )


@router.post("/documents")
async def execute_documents_query(
    query: QueryRequest,
    top_k: int = 10,
) -> QueryResponse:
    """
    Execute a query to get the documents that match the query.

    Args:
        query(QueryRequest): The query to execute.
        top_k(int): The number of documents to return.

    Returns:
        (QueryResponse): The response containing the status and message.
    """
    rag_service = RagService()
    sources = rag_service.retrieve(query.query, top_k=top_k)
    return QueryResponse(
        sources=sources,
    )
