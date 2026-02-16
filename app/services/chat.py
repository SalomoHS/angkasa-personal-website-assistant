from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler

from app.models.chat import ChatResponse, ChatValidationResponse
from app.core.prompts import ask_prompt, val_prompt
from app.core.config import config
from app.vendor.vector_db import retriever
from app.vendor.ai import llm

Langfuse(
    public_key=config.LANGFUSE_PUBLIC_KEY,
    secret_key=config.LANGFUSE_SECRET_KEY,
    host=config.LANGFUSE_BASE_URL  # Optional: defaults to https://cloud.langfuse.com
)

# Get the configured client instance
langfuse = get_client()

# Initialize the Langfuse handler
langfuse_handler = CallbackHandler()

class ChatService():
    def __init__(self):
        self.ask_prompt = ChatPromptTemplate.from_messages([
            ("system", ask_prompt),
            MessagesPlaceholder(variable_name="chat_history")
        ])
        self.ask_chain = (
            {"context": (lambda x: x['chat_history'][-1].content) | retriever, "chat_history": lambda x: x['chat_history']}
            | self.ask_prompt
            | llm
            | StrOutputParser()
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

    async def send_message(self, chat_history: list, query: str) -> ChatResponse:
        # validation = await self.validate_message(query)
        # if validation.status == "invalid":
        #     return ChatResponse(response=validation.response)
        
        parsed_chat_history = self.parse_chat_history(chat_history, query)
        response_text = self.ask_chain.invoke(
            {"chat_history": parsed_chat_history},
            config={"callbacks": [langfuse_handler]}
        )
        return ChatResponse(response=response_text)

    async def stream_message(self, chat_history: list, query: str):
        parsed_chat_history = self.parse_chat_history(chat_history, query)
        async for chunk in self.ask_chain.astream(
            {"chat_history": parsed_chat_history},
            config={"callbacks": [langfuse_handler]}
        ):
            yield chunk

