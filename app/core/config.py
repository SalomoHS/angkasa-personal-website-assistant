from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv
load_dotenv()

class Config(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv('GOOGLE_API_KEY')
    LANGUAGE_MODEL_NAME: str = os.getenv('LANGUAGE_MODEL_NAME')
    EMBEDDING_MODEL_NAME: str = os.getenv('EMBEDDING_MODEL_NAME')

    PINECONE_API_KEY: str = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME: str = os.getenv('PINECONE_INDEX_NAME')

    LANGFUSE_SECRET_KEY: str = os.getenv('LANGFUSE_SECRET_KEY')
    LANGFUSE_PUBLIC_KEY: str = os.getenv('LANGFUSE_PUBLIC_KEY')
    LANGFUSE_BASE_URL: str = os.getenv('LANGFUSE_BASE_URL')

config = Config()