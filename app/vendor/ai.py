from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from app.core.config import config

def get_embeddings(langfuse_prompt):
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=config.GOOGLE_API_KEY, model=langfuse_prompt.config["embedding_model"], output_dimensionality=langfuse_prompt.config["embedding_dimensions"])
    return embeddings

def get_llm(langfuse_prompt):
    llm = GoogleGenerativeAI(google_api_key=config.GOOGLE_API_KEY, model=langfuse_prompt.config["model"], temperature=langfuse_prompt.config["temperature"], max_tokens=langfuse_prompt.config["max_tokens"])
    return llm