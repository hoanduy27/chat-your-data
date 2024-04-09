import io
import os
import json
import pickle
import streamlit as st

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, PyPDFLoader, WebBaseLoader
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


from langchain_community.document_loaders import pdf


import pdb

from data import *

from typing import Union, List

from loader import PyPDFByteLoader, TextLoader

def postprocess(text):
  text = text.split('\n')
  text = [line for line in text if line != '']

  return '\n'.join(text)

class KnowledgeBase:
    def __init__(self, name, documents=None):
        self.name = name

        if documents:
            self.documents = documents 
        else:
            self.documents = []

        self.pages = [] 
        self.embedding = None 
        self.embedding_config = None 

    def add_document(
            self, 
            documents: Union[Document, List[Document]]
        ):
        if isinstance(documents, list):
            self.documents.extend(documents)
        else:
            self.documents.append(documents)

    def set_embedding(self, embedding_name, context: dict):
        print("SEtting embedding")
        embedding_class = embedding_choices[embedding_name]

        if embedding_name == "OpenAI":
            os.environ["OPENAI_API_KEY"] = context['api_key']
            self.embedding = embedding_class()
            context.pop('api_key')
            
        else:
            # print(context)
            self.embedding = embedding_class(**context)

        self.embedding_config = {
            "class": embedding_name,
            "config": context
        }

    def load_document(self):
        loaders = []
        for doc in self.documents:
            if doc.type == FILE:
                if doc.data.name.endswith('pdf'):
                    fs = io.BytesIO()
    
                    fs.write(doc.data.getvalue())
                    fs.seek(0)
                    
                    loaders.append(PyPDFByteLoader(fs))

            elif doc.type == URL:
                try:
                    loader = WebBaseLoader(doc.data)
                    loader.requests_kwargs = {'verify' :False}
                                              
                    loaders.append(loader)
                except:
                    pass

            elif doc.type == TEXT:
                if doc.data != "":
                    # fs = io.BytesIO()        
                    # fs.write(doc.data.encode("utf-8"))
                    
                    loaders.append(TextLoader(doc.data))
        
        for loader in loaders:
            try:
                self.pages.extend(loader.load())
            except:
                print(f"{loader} failed!")
                continue

        return self.pages
        

    def split_document(self):
        # self.pages will be splitted to smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        self.pages = text_splitter.split_documents(self.pages)

    def embed_document(self):
        os.makedirs(VECTORSTORE_ROOT, exist_ok=True)
        
        savedir = os.path.join(
            VECTORSTORE_ROOT,
            self.name
        )
        
        # embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectorstore = FAISS.from_documents(self.pages, self.embedding)
        
        self.vectorstore.save_local(os.path.join(VECTORSTORE_ROOT, self.name))
        
        with open(os.path.join(savedir, 'embedding_config.json'), 'w') as f:
            json.dump(self.embedding_config, f, indent=2)
        # with open(os.path.join(VECTORSTORE_ROOT, self.name + '.pkl'), "wb") as f:
        #     pickle.dump(self.vectorstore, f)

if __name__ =="__main__":
    print("Loading data...")
    loader = UnstructuredFileLoader("state_of_the_union.txt")
    raw_documents = loader.load()


    print("Splitting text...")
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
    )
    documents = text_splitter.split_documents(raw_documents)


    print("Creating vectorstore...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)
