"""
Game management router for Veritaminal API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..models import (
    StartGameRequest, StartGameResponse, 
    SaveGameRequest, SaveGameResponse,
    LoadGameResponse, SettingsResponse, GameState
)
from ..services import game_service, auth_service
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/start", response_model=StartGameResponse)
async def start_game(request: StartGameRequest):
    """Start a new game with the specified border setting"""
    # Create a new game ID
    game_id = str(uuid.uuid4())
    
    # Get border setting
    setting = game_service.get_border_setting(request.setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Border setting with ID {request.setting_id} not found."
        )
    
    # Initialize game state
    game_service.initialize_game(game_id, setting)
    
    return {
        "game_id": game_id,
        "setting": setting,
        "day": 1
    }

@router.post("/save", response_model=SaveGameResponse)
async def save_game(request: SaveGameRequest):
    """Save the current game state"""
    if not game_service.game_exists(request.game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {request.game_id} not found."
        )
    
    # Generate save ID and timestamp
    save_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Save game state
    game_service.save_game(save_id, request.game_state, timestamp)
    
    return {
        "save_id": save_id,
        "timestamp": timestamp
    }

@router.get("/load/{save_id}", response_model=LoadGameResponse)
async def load_game(save_id: str = Path(...)):
    """Load a saved game"""
    saved_game = game_service.load_game(save_id)
    if not saved_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Saved game with ID {save_id} not found."
        )
    
    return {
        "game_state": saved_game
    }

@router.get("/settings", response_model=SettingsResponse)
async def get_settings():
    """Get available border settings"""
    settings = game_service.get_all_border_settings()
    
    return {
        "settings": settings
    }