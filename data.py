from dataclasses import dataclass
from typing import Any
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

@dataclass
class Document:
    type: str
    data: Any

FILE = "file"
URL = "url"
TEXT = "text"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

VECTORSTORE_ROOT = "assets"

embedding_choices = {
    "OpenAI": {
        "class": OpenAIEmbeddings,
        "context": {
            "api_key": "API KEY"
        }
    },
    "HuggingFace": {
        "class": HuggingFaceEmbeddings,
        "context": {
            "model_name": "Model Name"
        }
    }
}