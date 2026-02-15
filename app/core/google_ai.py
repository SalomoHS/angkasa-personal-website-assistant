from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
model = os.environ.get("MODEL_NAME")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", output_dimensionality=1024)
llm = GoogleGenerativeAI(model=model, google_api_key=google_api_key, temperature=0.7)

with open("app/core/system_prompt/ask_prompt.txt", "r") as f:
    ask_prompt = f.read()

with open("app/core/system_prompt/val_prompt.txt", "r") as f:
    val_prompt = f.read()

