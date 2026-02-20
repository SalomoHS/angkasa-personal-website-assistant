# Personal Website Assistant

## Architecture
![ANGKASA ARCHITECTURE](https://github.com/user-attachments/assets/2fc12e03-6c96-410b-b954-015b68fdc22c)

## Project Overview

This is my personal website assistant to make personal website visitor can explore Salomo Hendrian Sudjono's project, skill, and background via chatbot.

## File Structure

```
.
├── app/                    # Main Application Logic
│   ├── api/                # API Route Definitions
│   │   └── v1/             # Version 1 API endpoints
│   │       └── chat.py     # Chat API endpoints
│   ├── core/               # Configuration & Core Settings
│   │   └── config.py       # Environment variables & app config
│   ├── models/             # Data Models (Pydantic)
│   │   └── chat.py         # Chat request/response models
│   ├── services/           # Business Logic Services
│   │   └── chat.py         # RAG implementation & chat logic
│   ├── vendor/             # External Service Integrations
│   │   ├── ai.py           # Google Generative AI setup
│   │   ├── llm_trace.py    # Langfuse tracing integration
│   │   └── vector_db.py    # Pinecone vector store setup
│   └── main.py             # FastAPI Application Entry Point
├── requirements.txt        # Python Dependencies
├── pyproject.toml          # Python Project Metadata
├── uv.lock                 # Python Dependency Lock File
```

## Try it on

Check out the assistant live on my personal website:
[https://personal-website-theta-roan.vercel.app](https://personal-website-theta-roan.vercel.app)
