"""
Authentication service for Veritaminal API
"""

from typing import Dict, Optional
from ..models import SessionData

# In-memory store for active sessions
# In a production environment, this would be a database
active_sessions: Dict[str, SessionData] = {}

def create_session(session_id: str, api_key: str) -> None:
    """
    Create a new session with the given API key
    
    Args:
        session_id (str): The session ID to create
        api_key (str): The API key to associate with the session
    """
    active_sessions[session_id] = SessionData(
        session_id=session_id,
        api_key=api_key
    )

def get_session(session_id: str) -> Optional[SessionData]:
    """
    Get session data by session ID
    
    Args:
        session_id (str): The session ID to retrieve
        
    Returns:
        Optional[SessionData]: The session data, or None if not found
    """
    return active_sessions.get(session_id)

def validate_session(session_id: str) -> bool:
    """
    Validate that a session exists
    
    Args:
        session_id (str): The session ID to validate
        
    Returns:
        bool: True if the session is valid, False otherwise
    """
    return session_id in active_sessions

def delete_session(session_id: str) -> None:
    """
    Delete a session
    
    Args:
        session_id (str): The session ID to delete
    """
    if session_id in active_sessions:
        del active_sessions[session_id]