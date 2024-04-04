import streamlit as st

from data import *

from ingestor import KnowledgeBase
import pdb

class Session:
    def __init__(self):
        self.knowledge_base = None 

    def render_sidebar(self):
        st.sidebar.markdown("# Collections")
        name = st.sidebar.text_input("Your collection name (required, mate!)")
        files = st.sidebar.file_uploader("Files (PDF only now)", accept_multiple_files=True)

        urls = st.sidebar.text_area("Web pages (new line for each url)")

        text = st.sidebar.text_area("Custom message")

        if st.sidebar.button("Generate"):
            self.knowledge_base = KnowledgeBase(name)
            
            for f in files:
                self.knowledge_base.add_document(Document(
                    type=FILE, data=f
                ))
            
            for url in urls.split('\n'):
                self.knowledge_base.add_document(Document(
                    type=URL, data=url
                ))

            self.knowledge_base.add_document(Document(
                type=TEXT, data=text
            ))

            self.knowledge_base.load_document()
            self.knowledge_base.split_document()
            self.knowledge_base.embed_document()

        

    def render(self):
        self.render_sidebar()


session = Session()

session.render()