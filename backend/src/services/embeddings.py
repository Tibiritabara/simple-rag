"""
Set of services to handle the embeddings of documents and the creation of a vector store.
"""

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from pydantic import BaseModel, PrivateAttr
from weaviate import WeaviateClient, connect_to_local

from utils.config import get_config


class VectorStoreHandler(BaseModel):
    """
    Embeds text using the OpenAI API.
    It also handles the creation of a vector store and the insertion of documents into it.
    It also provides a method to get the index of the vector store.

    Attributes:
        index_name(str): The name of the index to use
    """

    index_name: str
    __weaviate_client: WeaviateClient = PrivateAttr()
    __embed_model: AzureOpenAIEmbedding = PrivateAttr()

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
        self.__embed_model = AzureOpenAIEmbedding(
            api_key=get_config().azure_openai_api_key.get_secret_value(),
            endpoint=get_config().azure_openai_endpoint,
            model=get_config().azure_openai_embeddings_model,
            api_version=get_config().azure_openai_api_version,
        )

    def from_documents(self, documents: list[Document]) -> VectorStoreIndex:
        """
        Embed a list of LlamaIndex documents and store them in a vector store.

        Args:
            documents(list[Document]): The documents to embed

        Returns:
            (VectorStoreIndex): The VectorStoreIndex from LlamaIndex
        """
        vector_store = WeaviateVectorStore(
            weaviate_client=self.__weaviate_client,
            index_name=self.index_name,
        )

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
        )
        index = VectorStoreIndex(
            nodes=documents,
            storage_context=storage_context,
            embed_model=self.__embed_model,
        )

        return index

    def get_index(self) -> VectorStoreIndex:
        """
        Get the index of the vector store.

        Returns:
            (VectorStoreIndex): The VectorStoreIndex from LlamaIndex
        """
        vector_store = WeaviateVectorStore(
            weaviate_client=self.__weaviate_client,
            index_name=self.index_name,
        )

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
        )
        index = VectorStoreIndex(
            nodes=[],
            storage_context=storage_context,
            embed_model=self.__embed_model,
        )

        return index
