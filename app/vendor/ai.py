from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from app.core.config import config

embeddings = GoogleGenerativeAIEmbeddings(google_api_key=config.GOOGLE_API_KEY, model=config.EMBEDDING_MODEL_NAME, output_dimensionality=1024)
llm = GoogleGenerativeAI(google_api_key=config.GOOGLE_API_KEY, model=config.LANGUAGE_MODEL_NAME, temperature=0.7, max_tokens=2048)