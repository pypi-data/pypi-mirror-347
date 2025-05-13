"""
Gameplay router for Veritaminal API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..models import (
    DocumentRequest, DocumentResponse,
    DecisionRequest, DecisionResponse,
    HintRequest, HintResponse,
    NextDayRequest, NextDayResponse
)
from ..services import game_service, gameplay_service, ai_service, narrative_service

router = APIRouter()

@router.post("/document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """Generate a document for the current game"""
    # Check if game exists
    if not game_service.game_exists(request.game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {request.game_id} not found."
        )
    
    # Get game state
    game_state = game_service.get_game_state(request.game_id)
    
    # Generate document
    document = gameplay_service.generate_document(game_state)
    
    # Get AI judgment
    ai_judgment = ai_service.judge_document(document, game_state)
    
    # Update game state with current document
    game_service.set_current_document(request.game_id, document)
    
    return {
        "document": document,
        "ai_judgment": ai_judgment
    }

@router.post("/decision", response_model=DecisionResponse)
async def make_decision(request: DecisionRequest):
    """Make a decision (approve/deny) for a document"""
    # Check if game exists
    if not game_service.game_exists(request.game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {request.game_id} not found."
        )
    
    # Validate decision
    if request.decision not in ["approve", "deny"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision must be either 'approve' or 'deny'."
        )
    
    # Get game state and current document
    game_state = game_service.get_game_state(request.game_id)
    document = game_service.get_current_document(request.game_id)
    
    # Check if document exists
    if not document or document.id != request.document_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {request.document_id} not found or not current."
        )
    
    # Process decision
    is_correct, points = gameplay_service.process_decision(
        game_state, document, request.decision
    )
    
    # Generate narrative update
    narrative_update = narrative_service.generate_update(
        game_state, document, request.decision, is_correct
    )
    
    # Update game state
    updated_game_state = game_service.update_game_state_after_decision(
        request.game_id, document, request.decision, is_correct, points, narrative_update
    )
    
    return {
        "is_correct": is_correct,
        "points": points,
        "narrative_update": narrative_update,
        "game_state": updated_game_state
    }

@router.post("/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    """Get a hint for the current document"""
    # Check if game exists
    if not game_service.game_exists(request.game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {request.game_id} not found."
        )
    
    # Get game state and current document
    game_state = game_service.get_game_state(request.game_id)
    document = game_service.get_current_document(request.game_id)
    
    # Check if document exists
    if not document or document.id != request.document_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {request.document_id} not found or not current."
        )
    
    # Generate hint
    hint = ai_service.generate_hint(document, game_state)
    
    return {
        "hint": hint
    }

@router.post("/next-day", response_model=NextDayResponse)
async def advance_day(request: NextDayRequest):
    """Advance to the next day"""
    # Check if game exists
    if not game_service.game_exists(request.game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {request.game_id} not found."
        )
    
    # Get game state
    game_state = game_service.get_game_state(request.game_id)
    
    # Check if game is over
    if game_state.is_game_over:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already over."
        )
    
    # Advance to next day
    next_day = game_state.day + 1
    is_game_over = next_day > 10  # Game ends after day 10
    
    # Generate day message
    day_message = narrative_service.generate_day_message(next_day, game_state)
    
    # Update game state
    updated_game_state = game_service.advance_day(request.game_id, next_day, day_message)
    
    # Check for game over
    ending_type = None
    ending_message = None
    
    if is_game_over:
        ending_type, ending_message = narrative_service.generate_ending(updated_game_state)
        game_service.end_game(request.game_id, ending_type)
    
    return {
        "day": next_day,
        "day_message": day_message,
        "is_game_over": is_game_over,
        "ending_type": ending_type,
        "ending_message": ending_message
    }