"""
FastAPI server implementation for the Gemini chat plugin.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from .api import ChatHandler, ChatError, FileAccessError, ModelError

app = FastAPI(title="MkDocs Gemini Chat API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be configured in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import aioredis

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool('redis://localhost')
    await FastAPILimiter.init(redis)

# API key authentication
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if not api_key or api_key != os.getenv("GEMINI_API_KEY"):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    filePath: Optional[str] = None
    language: str = "en"
    version: str = "latest"
    history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    text: str
    success: bool
    error: Optional[str] = None
    metadata: Optional[Dict] = None

# Chat handler instance
chat_handler = None

@app.on_event("startup")
async def initialize_chat_handler():
    global chat_handler
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    chat_handler = ChatHandler(api_key)

# Endpoints
@app.post("/api/chat", response_model=ChatResponse)
@RateLimiter(times=10, seconds=60)  # 10 requests per minute
async def chat(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Handle chat requests.
    
    Args:
        request: ChatRequest object containing message and optional parameters
        api_key: API key for authentication
        
    Returns:
        ChatResponse object containing the response text and metadata
        
    Raises:
        HTTPException: For various error conditions
    """
    try:
        # Validate file path if provided
        if request.filePath:
            if not os.path.exists(request.filePath) or not os.path.isfile(request.filePath):
                raise FileAccessError(f"Invalid file path: {request.filePath}")
            
            # Basic path traversal protection
            abs_path = os.path.abspath(request.filePath)
            if not abs_path.startswith(os.getcwd()):
                raise FileAccessError("File path outside allowed directory")

        response = await chat_handler.handle_message(
            message=request.message,
            file_path=request.filePath,
            language=request.language,
            version=request.version,
            history=request.history
        )
        
        return ChatResponse(
            text=response.text,
            success=True,
            metadata=response.metadata
        )
        
    except FileAccessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ModelError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ChatError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") 