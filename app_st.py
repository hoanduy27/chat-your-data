import streamlit as st
import pdb
import io
from dataclasses import dataclass
from ingestor import load_documents

from typing import Any
from data import *

from ingestor import KnowledgeBase

class Session:
    def __init__(self):
        self.knowledge_base = None 

    def render_sidebar(self):
        st.sidebar.markdown("# Collections")
        files = st.sidebar.file_uploader("Files (PDF only now)", accept_multiple_files=True)

        urls = st.sidebar.text_area("Web pages (new line for each url)")

        text = st.sidebar.text_area("Custom message")

        if st.button("Generate"):
            self.knowledge_base = KnowledgeBase()
            for f in files:
                self.knowledge_base.add_document(Document(
                    type=FILE, data=f
                ))
            
            for url in urls:
                self.knowledge_base.add_document(Document(
                    type=URL, data=url
                ))

            self.knowledge_base.add_document(Document(
                type=TEXT, data=text
            ))

            self.knowledge_base.load_document()

        

    def render(self):
        self.render_sidebar()


session = Session()

session.render()