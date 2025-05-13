"""
Gameplay service for Veritaminal API

Handles core gameplay mechanics including document generation and decision processing.
"""

import uuid
import random
from typing import Dict, List, Optional, Tuple
from ..models import Document, GameState
import sys
import os

# Add the game module to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from game import api as game_api

def generate_document(game_state: GameState) -> Document:
    """
    Generate a document based on the current game state
    
    Args:
        game_state (GameState): The current game state
        
    Returns:
        Document: The generated document
    """
    # Create context for document generation based on previous travelers
    used_names_context = ""
    if game_state.traveler_history:
        used_names = [traveler.document.name for traveler in game_state.traveler_history]
        used_names_context = f"Previously seen travelers: {', '.join(used_names)}"
    
    # Get border setting for document generation
    setting = game_state.border_setting
    
    # Generate document using the original game API
    name, permit, backstory, additional_fields = game_api.generate_document_for_setting(
        {
            "name": setting.name,
            "situation": setting.situation,
            "document_requirements": setting.document_requirements,
            "common_issues": setting.common_issues
        },
        used_names_context
    )
    
    # Determine if permit is valid (P followed by 4 digits)
    is_valid = len(permit) == 5 and permit[0] == 'P' and permit[1:].isdigit()
    
    # Create document
    document = Document(
        id=str(uuid.uuid4()),
        name=name,
        permit=permit,
        backstory=backstory,
        additional_fields=additional_fields,
        is_valid=is_valid
    )
    
    return document

def process_decision(game_state: GameState, document: Document, decision: str) -> Tuple[bool, int]:
    """
    Process a player's decision on a document
    
    Args:
        game_state (GameState): The current game state
        document (Document): The document being decided on
        decision (str): The player's decision (approve/deny)
        
    Returns:
        Tuple[bool, int]: A tuple containing (is_correct, points)
    """
    # Get the correct decision based on document validity
    correct_decision = "approve" if document.is_valid else "deny"
    
    # Determine if the player's decision was correct
    is_correct = decision == correct_decision
    
    # Calculate points based on correctness and game state
    base_points = 10
    
    # Bonus points based on game progression (harder days = more points)
    day_multiplier = min(2.0, 1.0 + (game_state.day - 1) * 0.1)
    
    # Penalty for incorrect decisions
    correctness_multiplier = 1.0 if is_correct else -0.5
    
    # Calculate total points
    points = int(base_points * day_multiplier * correctness_multiplier)
    
    return is_correct, points