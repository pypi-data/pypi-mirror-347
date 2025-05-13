"""
Authentication router for Veritaminal API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..models import InitializeRequest, InitializeResponse
import uuid
from ..services import auth_service

router = APIRouter()

@router.post("/initialize", response_model=InitializeResponse)
async def initialize(request: InitializeRequest):
    """Initialize a session with an API key"""
    # Validate API key (in a production environment, you'd verify against a database)
    if not request.api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API key is required."
        )
    
    # Create a session ID for this authenticated session
    session_id = str(uuid.uuid4())
    
    # Store session
    auth_service.create_session(session_id, request.api_key)
    
    return {
        "status": "success",
        "session_id": session_id
    }