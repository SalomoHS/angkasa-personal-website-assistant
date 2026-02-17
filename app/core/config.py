from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv
load_dotenv()

class Config(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv('GOOGLE_API_KEY')

    PINECONE_API_KEY: str = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME: str = os.getenv('PINECONE_INDEX_NAME')

    LANGFUSE_SECRET_KEY: str = os.getenv('LANGFUSE_SECRET_KEY')
    LANGFUSE_PUBLIC_KEY: str = os.getenv('LANGFUSE_PUBLIC_KEY')
    LANGFUSE_BASE_URL: str = os.getenv('LANGFUSE_BASE_URL')

    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    os.environ["LANGFUSE_TRACING_ENVIRONMENT"] = ENVIRONMENT
    os.environ["OTEL_SERVICE_NAME"] = os.getenv('OTEL_SERVICE_NAME', 'ask-angkasa')

    ANGKASA_HOST: str = os.getenv('ANGKASA_HOST')

config = Config()