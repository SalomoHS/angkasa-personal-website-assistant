from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1 import chat
from app.core.config import config
from app.vendor.llm_trace import get_langfuse_client, get_langfuse_prompt, get_langfuse_callback_handler, get_propagate_attributes
from app.vendor.ai import get_embeddings, get_llm
from app.vendor.vector_db import get_retrieval

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.langfuse_client = get_langfuse_client()
    app.state.langfuse_prompt = get_langfuse_prompt(
        "angkasa-personal-website-assistant",
        label=["production"]
    )

    app.state.embeddings = get_embeddings(app.state.langfuse_prompt)
    app.state.llm = get_llm(app.state.langfuse_prompt)
    app.state.retriever = get_retrieval(app.state.langfuse_prompt)
    
    app.state.langfuse_callback_handler = get_langfuse_callback_handler()
    app.state.propagate_attributes = get_propagate_attributes()
    
    yield
    app.state.llm = None
    app.state.retriever = None
    app.state.langfuse_client = None
    app.state.langfuse_prompt = None
    app.state.langfuse_callback_handler = None
    app.state.propagate_attributes = None

app = FastAPI(lifespan=lifespan)

origins = ["*"]

if config.ENVIRONMENT == "production":
    origins = [
        "https://personal-website-theta-roan.vercel.app",
        "https://personal-website-theta-roan.vercel.app/"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(chat.router, prefix="/api/v1")