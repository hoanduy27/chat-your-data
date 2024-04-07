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

NEW_COLLECTION = "Create new collection"
LOAD_COLLECTIONS = "Load existing collections"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

VECTORSTORE_ROOT = "assets"

embedding_choices = {
    "OpenAI": OpenAIEmbeddings,
    "HuggingFace": HuggingFaceEmbeddings
}

chat_options = ['gpt-4', 'gpt-3.5-turbo']

embedding_args = {
    "OpenAI": {
        "api_key": "API KEY"
    },
    "HuggingFace": {
        "model_name": "Model Name"
    }
}

MAX_HISTORY = 3