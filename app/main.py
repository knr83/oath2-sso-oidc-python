import logging

logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.config import settings

app = FastAPI(title="Azure AD Auth Demo", version="0.1.0")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication router
app.include_router(auth_router, prefix="/auth")


@app.get("/test")
async def test_endpoint():
    return {"message": "CORS is working"}
