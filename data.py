from dataclasses import dataclass
from typing import Any

@dataclass
class Document:
    type: str
    data: Any

FILE = "file"
URL = "url"
TEXT = "text"