from langfuse import Langfuse, get_client, propagate_attributes
from langfuse.langchain import CallbackHandler
from app.core.config import config

Langfuse(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_BASE_URL,
        timeout=10
    )

def get_langfuse_client():
    langfuse = get_client()
    return langfuse

def get_langfuse_callback_handler():
    langfuse_handler = CallbackHandler()
    return langfuse_handler

def get_langfuse_prompt(prompt_name: str, label: list[str] = None):
    langfuse = get_langfuse_client()
    prompt = langfuse.get_prompt(prompt_name, label=label)
    return prompt

def get_propagate_attributes():
    return propagate_attributes