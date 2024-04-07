import streamlit as st

from data import *

from ingestor import KnowledgeBase
from query_data import QA, load_retriever
import pdb

import os 
import json
import openai

def get_reply():
    pass 

class Session:
    # def __init__(self):
    #     self.knowledge_base = None
    #     self.retriever = None  
    #     self.chain = None 

    def render_vectorstore_loader(self):
        vectorstore_list = os.listdir(VECTORSTORE_ROOT)

        vectorstore_name = st.sidebar.selectbox("Choose collection", vectorstore_list)

        vectorstore_path = os.path.join(VECTORSTORE_ROOT, vectorstore_name)

        with open(os.path.join(vectorstore_path, 'embedding_config.json'), 'r') as f:
            config = json.load(f)

            if config['class'] == "OpenAI":
                os.environ["OPENAI_API_KEY"] = st.sidebar.text_input("OPENAI API KEY")

        if st.sidebar.button("Load"):
            print(openai.api_key)
            st.session_state.retriever = load_retriever(vectorstore_path)
        
    def render_vectorstore_generator(self):
        st.sidebar.markdown("# Collections")
        name = st.sidebar.text_input("Your collection name (required, mate!)")
        files = st.sidebar.file_uploader("Files (PDF only now)", accept_multiple_files=True)

        urls = st.sidebar.text_area("Web pages (new line for each url)")

        text = st.sidebar.text_area("Custom message")

        st.sidebar.markdown("# Embeddings")
        embedding_name = st.sidebar.selectbox(
            "Choose embedding model", 
            options=embedding_args.keys()
        )
        context = {} 

        for param, value in embedding_args[embedding_name].items():
            context[param] = st.sidebar.text_input(value)
        
        if st.sidebar.button("Generate"):
            print("Create embedding...")
            st.session_state.knowlege_base = KnowledgeBase(name)
                
            st.session_state.set_embedding(embedding_name, context)
            
            for f in files:
                st.session_state.add_document(Document(
                    type=FILE, data=f
                ))
    
            for url in urls.split('\n'):
                st.session_state.add_document(Document(
                    type=URL, data=url
                ))

            st.session_state.add_document(Document(
                type=TEXT, data=text
            ))

            st.session_state.load_document()
            st.session_state.split_document()
            st.session_state.embed_document()

            st.session_state.retriever = load_retriever(self.vectorstore)
                

    def render_sidebar(self):
        selection = st.sidebar.selectbox("Collection selection", [NEW_COLLECTION, LOAD_COLLECTIONS])

        if selection == NEW_COLLECTION:
            self.render_vectorstore_generator()
        else:
            self.render_vectorstore_loader()

    def render_message_box(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "history" not in st.session_state:
            st.session_state.history = []

        if st.sidebar.button("Clear context"):
            st.session_state.history = []            

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is up?"):
            print(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            reply, history =  st.session_state.qa.reply(
                prompt, 
                st.session_state.history
            )

            st.session_state.history = history

            if len(st.session_state.history) // 2 >= MAX_HISTORY:
                st.session_state.history = []
                st.session_state.qa.clear_context()

            if len(st.session_state.history) == 0:
                st.text("Context clear!")
            else:
                st.text(f"Context will be cleared after {MAX_HISTORY - len(st.session_state.history)//2} turns.") 

            print(f"{st.session_state.history}")

            # reply = "Text normalization, speech encoder and vocoder."

            st.session_state.messages.append({"role": "bot", "content": reply})

            with st.chat_message("bot"):
                st.markdown(reply)

    def render_chat(self):
        st.sidebar.markdown("# Chat model")
        chat_model = st.sidebar.selectbox("Choose chat model", chat_options)
        if st.sidebar.button("Start chit-chatting!"):
            st.session_state.qa = QA(st.session_state.retriever, chat_model)
            st.session_state.qa.get_chain()
            # pass

    def render_main(self):
        if "retriever" in st.session_state:
            self.render_chat()
            self.render_message_box()
            st.sidebar.text("Load success")

        else:
            # self.render_message_box()
            st.sidebar.text("Please load collection")

    def render(self):
        self.render_sidebar()
        self.render_main()

session = Session()

session.render()