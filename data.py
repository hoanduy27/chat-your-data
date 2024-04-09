from dataclasses import dataclass
from typing import Any
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
from uuid import uuid4
from langsmith import Client

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__0ad5987d8865411caa6f1088be2085b0"  # Update to your API key

Client()

@dataclass
class Document:
    type: str
    data: Any

FILE = "file"
URL = "url"
TEXT = "text"
JSON = "json"


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

EN = "English"
VI = "Vietnamese"