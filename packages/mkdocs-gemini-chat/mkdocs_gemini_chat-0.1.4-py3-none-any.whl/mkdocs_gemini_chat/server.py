"""
FastAPI server implementation for the Gemini chat plugin.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from contextlib import asynccontextmanager
from .api import ChatHandler, ChatError, FileAccessError, ModelError

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize API key and chat handler on startup
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    app.state.chat_handler = ChatHandler(api_key)
    yield
    # Cleanup on shutdown (if needed)
    app.state.chat_handler = None

app = FastAPI(title="MkDocs Gemini Chat API", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be configured in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key authentication
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )
    if api_key != os.getenv("GEMINI_API_KEY"):
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

# Endpoints
@app.post("/api/chat", response_model=ChatResponse)
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

        response = await app.state.chat_handler.handle_message(
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