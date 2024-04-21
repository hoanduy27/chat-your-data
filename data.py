from dataclasses import dataclass
from typing import Any
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings

import os
from uuid import uuid4
from langsmith import Client

from dotenv import load_dotenv

load_dotenv()

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT", "")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY", "") # Update to your API key

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