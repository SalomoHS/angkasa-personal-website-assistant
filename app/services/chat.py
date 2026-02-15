from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from app.models.chat import ChatResponse, ChatValidationResponse
from app.core.google_ai import llm, ask_prompt, val_prompt
from app.core.vector_db import retriever

class ChatService():
    def __init__(self):
        self.llm = llm
        self.ask_prompt = ChatPromptTemplate.from_messages([
            ("system", ask_prompt),
            MessagesPlaceholder(variable_name="chat_history")
        ])
        self.ask_chain = (
            {"context": retriever, "input": RunnablePassthrough(), "chat_history": RunnablePassthrough()}
            | self.ask_prompt
            | llm
            | PydanticOutputParser(pydantic_object=ChatResponse)
        )

        self.validate_prompt = ChatPromptTemplate.from_messages([
            ("system", val_prompt),
            ("human", "{input}")
        ])

        self.validate_chain = (
            {"input": RunnablePassthrough()}
            | self.validate_prompt
            | llm
            | PydanticOutputParser(pydantic_object=ChatValidationResponse)
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

    async def validate_message(self, query:str) -> ChatValidationResponse:
        response = self.validate_chain.invoke({
            "input": query
        })
        return response

    async def send_message(self, chat_history: list, query: str) -> ChatResponse:
        validation = await self.validate_message(query)
        if validation.status == "invalid":
            return ChatResponse(response=validation.response)
        
        parsed_chat_history = self.parse_chat_history(chat_history, query)
        response = self.ask_chain.invoke({
            "chat_history": parsed_chat_history
        })
        return ChatResponse(response=response)
