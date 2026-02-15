import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from app.core.google_ai import embeddings
from dotenv import load_dotenv
load_dotenv()

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=pinecone_api_key)
vectorstore = PineconeVectorStore(index_name=pinecone_index_name, embedding=embeddings)
retriever = vectorstore.as_retriever()