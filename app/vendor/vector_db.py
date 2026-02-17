import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from app.core.config import config
from app.vendor.ai import get_embeddings

def get_retrieval():
    embeddings = get_embeddings()
    pc = Pinecone(api_key=config.PINECONE_API_KEY)

    vectorstore = PineconeVectorStore(index_name=config.PINECONE_INDEX_NAME, embedding=embeddings)
    return vectorstore.as_retriever()