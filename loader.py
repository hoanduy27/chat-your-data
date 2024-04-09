from abc import ABC, abstractmethod
import io
from langchain_community.document_loaders.blob_loaders import Blob

from typing import Iterator, Optional, Union, Dict
from langchain_community.document_loaders.pdf import (
    BasePDFLoader,
    PyPDFParser,
    PyPDFLoader
)

from langchain_community.document_loaders.base import BaseLoader


from langchain_core.documents import Document

class PyPDFByteLoader(BasePDFLoader):
    def __init__(
        self,
        fs: io.BytesIO,
        password: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict] = None,
        extract_images: bool = False,
    ) -> None:
        """Initialize with a file path."""
        try:
            import pypdf  # noqa:F401
        except ImportError:
            raise ImportError(
                "pypdf package not found, please install it with " "`pip install pypdf`"
            )
        self.fs = fs 
        self.headers = headers
        self.parser = PyPDFParser(password=password, extract_images=extract_images)

    def lazy_load(self) -> Iterator[Document]:
        blob = Blob.from_data(self.fs.read())

        yield from self.parser.parse(blob)

class TextLoader(BaseLoader):
    def __init__(self, text):
        self.text = text 

    def lazy_load(self):
        yield Document(page_content=self.text)