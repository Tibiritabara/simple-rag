"""
Services to extract text from files or folders using the unstructured API container.
"""

import os
from pathlib import Path
from typing import Literal

import boto3
from llama_index.core.schema import Document
from llama_index.readers.file import UnstructuredReader
from pydantic import BaseModel, FilePath, PrivateAttr
from unstructured.partition.utils.constants import PartitionStrategy

from utils.config import get_config


class TextExtractor(BaseModel):
    """
    Extracts text from files or folders using the unstructured API container.
    """

    __unstructured_reader: UnstructuredReader = PrivateAttr()

    def __init__(self, **kwargs):
        """
        Initializes the text extractor.
        """
        super().__init__(**kwargs)
        self.__unstructured_reader = UnstructuredReader(
            url=str(get_config().unstructured_url),
            api_key=get_config().unstructured_api_key.get_secret_value(),
        )

    def extract_text_from_file(
        self,
        filepath: FilePath,
        strategy: Literal[
            "auto",
            "fast",
            "ocr_only",
            "hi_res",
        ] = PartitionStrategy.AUTO,
        chunking: bool = True,
        chunk_size: int = 1000,
    ) -> list[Document]:
        """
        Extracts text from a file using the unstructured API container.

        Args:
            strategy: The strategy to use for partitioning the file.
            chunking: Whether to chunk the file.
            chunk_size: The size of the chunks to use for chunking.

        Returns:
            The text extracted from the file.
        """
        unstructured_kwargs = {
            "filename": filepath,
            "strategy": strategy,
        }
        if chunking:
            unstructured_kwargs["max_chunk_size"] = chunk_size
            unstructured_kwargs["chunking_strategy"] = "by_title"
        documents = self.__unstructured_reader.load_data(
            file=filepath,
            unstructured_kwargs=unstructured_kwargs,
            split_documents=True,
        )
        return documents

    def extract_text_from_folder(
        self,
        folder: Path,
        strategy: Literal[
            "auto",
            "fast",
            "ocr_only",
            "hi_res",
        ] = PartitionStrategy.AUTO,
        chunking: bool = True,
        chunk_size: int = 1000,
    ) -> list[Document]:
        """
        Extracts text from a folder using the unstructured API container.

        Args:
            folder: The folder to extract text from.
            strategy: The strategy to use for partitioning the files.
            chunking: Whether to chunk the files.
            chunk_size: The size of the chunks to use for chunking.

        Returns:
            The text extracted from the folder.
        """
        if not folder.exists():
            raise FileNotFoundError(f"Folder {folder} does not exist.")
        documents = []
        for file in folder.glob("**/*"):
            documents.extend(
                self.extract_text_from_file(file, strategy, chunking, chunk_size)
            )
        return documents


class FileHandler(BaseModel):
    """
    Handles files in the Minio server.
    """

    __blob_client = PrivateAttr()

    def __init__(self, **kwargs):
        """
        Initializes the text extractor.
        """
        super().__init__(**kwargs)
        boto_session = boto3.Session(
            aws_access_key_id=get_config().storage_access_key.get_secret_value(),
            aws_secret_access_key=get_config().storage_secret_key.get_secret_value(),
        )
        self.__blob_client = boto_session.client(
            endpoint_url=str(get_config().storage_endpoint_url),
            service_name="s3",
        )

    def upload_to_blob(self, file_path: FilePath) -> str:
        """
        Stores a file in the Minio server using the boto3 library.

        Args:
            file_path (FilePath): The path to the file to store.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If there is an error storing the file.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        object_key = os.path.basename(file_path)
        self.__blob_client.upload_file(
            str(file_path),
            get_config().storage_bucket,
            object_key,
        )
        return object_key

    def download_from_blob(
        self,
        bucket: str,
        object_key: str,
        file_path: str,
    ) -> Path:
        """
        Download a file from an S3 bucket

        Args:
            bucket (str): Bucket to download from
            object_key (str): S3 object key
            file_path (str): File path to download to

        Returns:
            Path: local file path
        """
        with open(file_path, "wb") as f:
            self.__blob_client.download_fileobj(bucket, object_key, f)
        return Path(file_path)
