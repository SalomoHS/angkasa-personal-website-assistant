from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from fastapi import Request

from app.core.config import config

class ChatService():
    def __init__(self, request: Request):
        self.llm = request.app.state.llm
        self.retriever = request.app.state.retriever
        
        self.langfuse_client = request.app.state.langfuse_client
        self.langfuse_prompt = request.app.state.langfuse_prompt
        self.langfuse_callback_handler = request.app.state.langfuse_callback_handler
        self.propagate_attributes = request.app.state.propagate_attributes

        self.ask_prompt = ChatPromptTemplate.from_messages([
            ("system", self.langfuse_prompt.prompt),
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

    async def stream_message(self, session_id: str, chat_history: list, query: str):
        parsed_chat_history = self.parse_chat_history(chat_history, query)

        with self.langfuse_client.start_as_current_observation(as_type="span", name="ask-angkasa") as root_span:
            
            root_span.update(input={"query": query})
            root_span.update(metadata={"session.id": session_id, "http.host": config.ANGKASA_HOST})

            with self.propagate_attributes(
                session_id=session_id
            ):
                response = ""
                
                async for chunk in self.ask_chain.astream(
                    {"chat_history": parsed_chat_history},
                    config={"callbacks": [self.langfuse_callback_handler], 
                            "metadata": {
                                "session.id": session_id,
                                "http.host": config.ANGKASA_HOST
                            }}
                ):
                    yield chunk
                    response += chunk
                
                root_span.update(output={"response": response})

