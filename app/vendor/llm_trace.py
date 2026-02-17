from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from app.core.config import config

def init_langfuse():
    Langfuse(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_BASE_URL  
    )

    langfuse = get_client()
    langfuse_handler = CallbackHandler()
    return langfuse_handler