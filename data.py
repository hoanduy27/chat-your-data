from dataclasses import dataclass
from typing import Any

@dataclass
class Document:
    type: str
    data: Any

FILE = "file"
URL = "url"
TEXT = "text"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

VECTORSTORE_ROOT = "assets"