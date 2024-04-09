from langchain.prompts.prompt import PromptTemplate

from data import *

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assistant for answering questions about the context given belown. You are given the following question and extracted parts of a long document. Provide a conversational answer. The question starts with "> QUESTION" and ends with  "> END OF QUESTION". The extracted parts of a long document starts with "> CONTEXT" and ends with "> END OF CONTEXT". The answer need not to be inside any tags.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
> QUESTION: 
{question}
> END OF QUESTION
=========
> CONTEXT:
{context}
> END OF CONTEXT
=========
English Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=[
                           "question", "context"])



# prompt = {
#     'Vietnamese':{
#         'condense_prompt':
#         'qa_prompt':
#     } 
#     'English':
# }