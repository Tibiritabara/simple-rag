"""
Set of tools to manage, validate, and retrieve the application's configuration.
"""

from functools import lru_cache

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    """
    Core settings and configurations for the application to run.

    Attributes:
        host: The hostname of the application
        app_name: The name of the application
        port: The port of the application
        version: The version of the application
        frontend_host: The hostname of the frontend application
        unstructured_url: The URL of the unstructured API
        unstructured_api_key: The API key for the unstructured API
        weaviate_host: The hostname of the Weaviate cluster
        weaviate_port: The port of the Weaviate cluster
        weaviate_grpc_port: The gRPC port of the Weaviate cluster
        azure_openai_api_key: The API key for the Azure OpenAI
        azure_openai_endpoint: The endpoint for the Azure OpenAI
        azure_openai_embeddings_model: The model for the Azure OpenAI embeddings
        azure_openai_api_version: The API version for the Azure OpenAI
        azure_openai_llm_model: The model for the Azure OpenAI LLM
        openai_api_key: The API key for the OpenAI
        openai_embeddings_model: The model for the OpenAI embeddings
        openai_llm_model: The model for the OpenAI LLM
        storage_access_key: The access key for the blob storage
        storage_secret_key: The secret key for the blob storage
        storage_bucket: The bucket for the blob storage
        storage_endpoint_url: The endpoint URL for the blob storage
        temporal_host: The hostname of the Temporal server
        temporal_namespace: The namespace of the Temporal server
        temporal_queue: The queue of the Temporal server
    """

    # App settings
    host: str = Field(description="The hostname of the application", default="0.0.0.0")
    app_name: str = Field(description="The name of the application", default="RAG API")
    port: int = Field(description="The port of the application", default=8000)
    version: str = Field(description="The version of the application", default="0.1.0")
    frontend_host: str = Field(
        description="The hostname of the frontend application",
        default="http://localhost:3000",
    )

    # Unstructured settings
    unstructured_url: HttpUrl = Field(description="The URL of the unstructured API")
    unstructured_api_key: SecretStr = Field(
        description="The API key for the unstructured API"
    )

    # Weaviate settings
    weaviate_host: str = Field(description="The hostname of the Weaviate cluster")
    weaviate_port: int = Field(description="The port of the Weaviate cluster")
    weaviate_grpc_port: int = Field(description="The gRPC port of the Weaviate cluster")

    # Azure OpenAI Settings
    azure_openai_api_key: SecretStr = Field(
        description="The API key for the Azure OpenAI"
    )
    azure_openai_endpoint: HttpUrl = Field(
        description="The endpoint for the Azure OpenAI"
    )
    azure_openai_embeddings_model: str = Field(
        description="The model for the Azure OpenAI embeddings"
    )
    azure_openai_api_version: str = Field(
        description="The API version for the Azure OpenAI", default="2024-10-21"
    )
    azure_openai_llm_model: str = Field(
        description="The model for the Azure OpenAI LLM"
    )

    # OpenAI Settings
    openai_api_key: SecretStr = Field(description="The API key for the OpenAI")
    openai_embeddings_model: str = Field(
        description="The model for the OpenAI embeddings"
    )
    openai_llm_model: str = Field(description="The model for the OpenAI LLM")

    # Blob Storage
    storage_access_key: SecretStr = Field(
        description="The access key for the blob storage"
    )
    storage_secret_key: SecretStr = Field(
        description="The secret key for the blob storage"
    )
    storage_bucket: str = Field(description="The bucket for the blob storage")
    storage_endpoint_url: HttpUrl = Field(
        description="The endpoint URL for the blob storage"
    )

    # Temporal settings
    temporal_host: str = Field(description="The hostname of the Temporal server")
    temporal_namespace: str = Field(description="The namespace of the Temporal server")
    temporal_queue: str = Field(description="The queue of the Temporal server")


@lru_cache
def get_config() -> Environment:
    """
    Get the application's configuration.

    Returns:
        (Environment): The application's configuration
    """
    return Environment()  # type: ignore
