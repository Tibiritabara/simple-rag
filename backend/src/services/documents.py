"""
Set of services to handle the documents stored in the vector database.
"""

import uuid

from pydantic import BaseModel, PrivateAttr
from weaviate import WeaviateClient, connect_to_local
from weaviate.collections.classes.internal import (
    ObjectSingleReturn,
    QueryReturn,
)
from weaviate.collections.collection import Collection

from utils.config import get_config


class DocumentService(BaseModel):
    """
    Service to handle documents stored in the vector database.

    Attributes:
        index_name(str): The name of the index to use
    """

    index_name: str
    __weaviate_client: WeaviateClient = PrivateAttr()
    __weaviate_collection: Collection = PrivateAttr()

    def __init__(self, index_name: str = "Documents", **kwargs):
        """
        Initializes the vector store handler.

        Args:
            index_name(str): The name of the index to use
        """
        super().__init__(index_name=index_name, **kwargs)
        self.__weaviate_client = connect_to_local(
            host=get_config().weaviate_host,
            port=get_config().weaviate_port,
            grpc_port=get_config().weaviate_grpc_port,
        )
        self.__weaviate_collection = self.__weaviate_client.collections.get(
            index_name,
        )

    def get_document_by_id(self, doc_id: uuid.UUID) -> ObjectSingleReturn:
        """
        Get a document by its ID from the vector store.

        Args:
            doc_id(uuid.UUID): The ID of the document to retrieve.

        Returns:
            (ObjectSingleReturn): The document.

        Raises:
            Exception: If the document is not found.
        """
        result = self.__weaviate_collection.query.fetch_object_by_id(doc_id)

        if not result:
            raise Exception(f"Document with ID {doc_id} not found")

        return result

    def get_all_documents(self, skip: int = 0, limit: int = 10) -> QueryReturn:
        """
        Get all documents from the vector store with pagination.

        Args:
            skip(int): Number of documents to skip.
            limit(int): Maximum number of documents to return.

        Returns:
            (QueryReturn): List of documents.
        """
        result = self.__weaviate_collection.query.fetch_objects(
            limit=limit,
            offset=skip,
        )

        return result

    def get_document_count(self) -> int:
        """
        Get the total number of documents in the vector store.

        Returns:
            (int): The total number of documents.
        """
        result = self.__weaviate_collection.aggregate.over_all(total_count=True)
        return result.total_count or 0
