from langchain.prompts.prompt import PromptTemplate

from data import *
_template = """Dựa vào lịch sử cuộc hội thoại và câu hỏi dưới đây, hãy viết lại thành một câu hỏi mới duy nhất. Lịch sử cuộc hội thoại bắt đầu bằng "CHAT HISTORY", câu hỏi bắt đầu bằng "QUESTION"

CHAT HISTORY:
{chat_history}

QUESTION: {question}

Câu hỏi mới:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """
Bạn là một trợ lý AI để trả lời câu hỏi về ngữ cảnh được đưa ra dưới đây.
Bạn được cung cấp câu hỏi và các phần trích dẫn của một tài liệu dài. Hãy đưa ra một câu trả lời như một cuộc trò chuyện giữa người với người. Câu hỏi bắt đầu bằng "> QUESTION" và kết thúc bằng "> END OF QUESTION". Các phần trích dẫn của tài liệu dài bắt đầu bằng "> CONTEXT" và kết thúc bằng "> END OF CONTEXT". Câu trả lời không cần phải được đặt trong thẻ chỉ định. 
Nếu bạn không biết câu trả lời, chỉ cần nói "Hmm, tôi không chắc". Đừng cố gắng bịa đặt câu trả lời.
> QUESTION: 
{question}
> END OF QUESTION
=========
> CONTEXT:
{context}
> END OF CONTEXT
=========
Trả lời bằng tiếng Việt theo định dạng Markdown:
"""

QA_PROMPT = PromptTemplate(template=template, input_variables=[
                           "question", "context"])
