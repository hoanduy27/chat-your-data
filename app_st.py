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

        st.sidebar.markdown("# Embeddings")
        embedding_name = st.sidebar.selectbox(
            "Choose embedding model", 
            options=embedding_choices.keys()
        )
        context = {} 

        for param, value in embedding_choices[embedding_name]["context"].items():
            context[param] = st.sidebar.text_input(value)
        
        if st.sidebar.button("Generate"):
            self.knowledge_base = KnowledgeBase(name)
            
            self.knowledge_base.set_embedding(embedding_name, context)
            
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

    def render_main(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is up?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            reply = "Hello"

            st.session_state.messages.append({"role": "bot", "content": reply})

            with st.chat_message("bot"):
                st.markdown(reply)

    def render(self):
        self.render_sidebar()
        self.render_main()

session = Session()

session.render()