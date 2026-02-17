from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from app.vendor.vector_db import get_retrieval
from app.vendor.ai import get_llm
from app.vendor.llm_trace import get_langfuse_client, get_langfuse_prompt, get_langfuse_callback_handler, get_propagate_attributes
from app.core.config import config

class ChatService():
    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retrieval()
        
        self.langfuse_client = get_langfuse_client()
        self.langfuse_prompt = get_langfuse_prompt("angkasa-personal-website-assistant", label=["production"])
        self.langfuse_callback_handler = get_langfuse_callback_handler()
        self.propagate_attributes = get_propagate_attributes()

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

