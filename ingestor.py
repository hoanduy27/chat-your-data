import io
import pickle
import streamlit as st

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, PyPDFLoader, WebBaseLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from data import *

from typing import Union, List

class KnowledgeBase:
    def __init__(self, documents=None):
        if documents:
            self.documents = documents 
        else:
            self.documents = []

        self.pages = [] 

    def add_document(self, documents: Union[Document, List[Document]]):
        if isinstance(documents, list):
            self.documents.extend(documents)
        else:
            self.documents.append(documents)

    def load_document(self):
        loaders = []
        for doc in self.documents:
            if doc.type == FILE:
                if doc.data.name.endswith('pdf'):
                    fs = io.BytesIO()
                    fs.write(doc.data.getvalue())

                    loaders.append(PyPDFLoader(fs))

            elif doc.type == URL:
                try:
                    loaders.append(WebBaseLoader(doc.data))
                except:
                    pass
            elif doc.type == TEXT:
                fs = io.BytesIO() 
                fs.write(doc.data.getvalue())
                
                loaders.append(UnstructuredFileLoader(fs))
        
        for loader in loaders:
            self.pages.extend(loader.load())

        return self.pages
        

    def split_document(self):
        # self.pages will be splitted to smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            sepa
        )

    def embed_document(self):
        pass 


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
