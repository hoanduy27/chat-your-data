import os 
import json
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.chat_models import ChatOpenAI

from langchain.memory import ConversationBufferMemory
from data import *
import pickle
from langchain.vectorstores.faiss import FAISS

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
You can assume the question about the most recent state of the union address.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assistant for answering questions about the most recent state of the union address.
You are given the following extracted parts of a long document and a question. Provide a conversational answer.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not about the most recent state of the union, politely inform them that you are tuned to only answer questions about the most recent state of the union.
Lastly, answer the question as if you were a pirate from the south seas and are just coming back from a pirate expedition where you found a treasure chest full of gold doubloons.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=[
                           "question", "context"])

class QA:
    def __init__(self, retriever, model_name):
        self.retriever = retriever
        self.model_name = model_name
        self.memory = None 
        self.chain = None 

    
    def get_chain(self):
        print("Get chain")
        # llm = ChatOpenAI(model_name=self.model_name, temperature=0)

        # chain = RetrievalQA.from_chain_type(
        #     llm, 
        #     retriever=self.retriever
        # )

        llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True)
        
        # see: https://github.com/langchain-ai/langchain/issues/5890
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.retriever,
            memory=self.memory,
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT}
        )
    
    def reply(self, question, history=None):
        if self.chain is None:
            self.get_chain() 

        if history is not None:
            reply = self.chain({"question": question, "chat_history": history})
        else: 
            reply = self.chain({"question": question})

        print(f"{reply = }")
        return reply['answer'], reply['chat_history']

    def clear_context(self):
        if self.memory is not None:
            self.memory.clear()

def load_retriever(vectorstore_path):
    print("RTV loaded")
    # return 1
    with open(os.path.join(vectorstore_path, 'embedding_config.json'), 'r') as f:
        config = json.load(f)
    
    embedding_cls = embedding_choices[config['class']]()

    vectorstore = FAISS.load_local(vectorstore_path, embedding_cls, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs=dict(k=3, fetch_k=10))

    # retriever = VectorStoreRetriever(vectorstore=vectorstore)
    return retriever


def get_basic_qa_chain():
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    retriever = load_retriever()
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory)
    return model


def get_custom_prompt_qa_chain():
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    retriever = load_retriever()
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # see: https://github.com/langchain-ai/langchain/issues/6635
    # see: https://github.com/langchain-ai/langchain/issues/1497
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return model


def get_condense_prompt_qa_chain():
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    retriever = load_retriever()
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # see: https://github.com/langchain-ai/langchain/issues/5890
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return model


def get_qa_with_sources_chain():
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    retriever = load_retriever()
    history = []
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True)

    def model_func(question):
        # bug: this doesn't work with the built-in memory
        # hacking around it for the tutorial
        # see: https://github.com/langchain-ai/langchain/issues/5630
        new_input = {"question": question['question'], "chat_history": history}
        result = model(new_input)
        history.append((question['question'], result['answer']))
        return result

    return model_func


chain_options = {
    "basic": get_basic_qa_chain,
    "with_sources": get_qa_with_sources_chain,
    "custom_prompt": get_custom_prompt_qa_chain,
    "condense_prompt": get_condense_prompt_qa_chain
}
