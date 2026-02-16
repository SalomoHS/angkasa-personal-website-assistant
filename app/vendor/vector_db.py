import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from app.core.config import config
from app.vendor.ai import embeddings

pc = Pinecone(api_key=config.PINECONE_API_KEY)
vectorstore = PineconeVectorStore(index_name=config.PINECONE_INDEX_NAME, embedding=embeddings)
retriever = vectorstore.as_retriever()