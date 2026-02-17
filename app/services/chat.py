from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from app.core.prompts import ask_prompt
from app.vendor.vector_db import get_retrieval
from app.vendor.ai import get_llm
from app.vendor.llm_trace import init_langfuse


class ChatService():
    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retrieval()
        self.llm_trace = init_langfuse()

        self.ask_prompt = ChatPromptTemplate.from_messages([
            ("system", ask_prompt),
            MessagesPlaceholder(variable_name="chat_history")
        ])

        self.ask_chain = (
            {"context": (lambda x: x['chat_history'][-1].content) | self.retriever, "chat_history": lambda x: x['chat_history']}
            | self.ask_prompt
            | self.llm
            | StrOutputParser()
        )

    def parse_chat_history(self, chat_history: list, query: str):
        parsed_chat_history = []
        for msg in chat_history:
            if msg.role == "human":
                parsed_chat_history.append(HumanMessage(content=msg.content))
            else:
                parsed_chat_history.append(AIMessage(content=msg.content))
        
        parsed_chat_history.append(HumanMessage(content=query))
        return parsed_chat_history

    async def stream_message(self, chat_history: list, query: str):
        parsed_chat_history = self.parse_chat_history(chat_history, query)
        async for chunk in self.ask_chain.astream(
            {"chat_history": parsed_chat_history},
            config={"callbacks": [self.llm_trace]}
        ):
            yield chunk

