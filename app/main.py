from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat
from app.core.config import config
import uvicorn

app = FastAPI()

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

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=1234, reload=True)
