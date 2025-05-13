"""
Game service for Veritaminal API

Handles game state management, initialization, and border settings.
"""

import uuid
import json
from typing import Dict, List, Optional
import os
from datetime import datetime
from ..models import GameState, BorderSetting, Document, TravelerRecord, DecisionRecord, NarrativeEvent, RuleChange
import sys
import os

# Add the game module to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from game import settings as game_settings

# In-memory stores
# In a production environment, these would be database tables
active_games: Dict[str, GameState] = {}
current_documents: Dict[str, Document] = {}
saved_games: Dict[str, GameState] = {}
save_timestamps: Dict[str, str] = {}

def get_border_setting(setting_id: str) -> Optional[BorderSetting]:
    """
    Get a border setting by ID
    
    Args:
        setting_id (str): The ID of the border setting
        
    Returns:
        Optional[BorderSetting]: The border setting, or None if not found
    """
    # Convert original game settings to API model
    settings = get_all_border_settings()
    for setting in settings:
        if setting.id == setting_id:
            return setting
    return None

def get_all_border_settings() -> List[BorderSetting]:
    """
    Get all available border settings
    
    Returns:
        List[BorderSetting]: All available border settings
    """
    # Convert original game settings to API model
    settings = []
    for setting_id, setting_data in game_settings.BORDER_SETTINGS.items():
        settings.append(BorderSetting(
            id=setting_id,
            name=setting_data["name"],
            description=setting_data["description"],
            situation=setting_data["situation"],
            document_requirements=setting_data["document_requirements"],
            common_issues=setting_data["common_issues"]
        ))
    return settings

def initialize_game(game_id: str, setting: BorderSetting) -> GameState:
    """
    Initialize a new game with the given border setting
    
    Args:
        game_id (str): The game ID
        setting (BorderSetting): The border setting to use
        
    Returns:
        GameState: The initial game state
    """
    # Create initial game state
    game_state = GameState(
        day=1,
        corruption=0,
        trust=50,
        score=0,
        traveler_history=[],
        decisions=[],
        narrative_events=[],
        rule_changes=[],
        is_game_over=False,
        border_setting=setting
    )
    
    # Add initial narrative event
    day_message = f"Day 1: Welcome to {setting.name}. Your assignment begins today."
    game_state.narrative_events.append(NarrativeEvent(
        day=1,
        text=day_message,
        type="day_start"
    ))
    
    # Add initial rule
    game_state.rule_changes.append(RuleChange(
        day=1,
        description="All travelers must have a valid permit (P followed by 4 digits).",
        rule_id="permit_format"
    ))
    
    # Store game state
    active_games[game_id] = game_state
    
    return game_state

def game_exists(game_id: str) -> bool:
    """
    Check if a game exists
    
    Args:
        game_id (str): The game ID to check
        
    Returns:
        bool: True if the game exists, False otherwise
    """
    return game_id in active_games

def get_game_state(game_id: str) -> Optional[GameState]:
    """
    Get the current state of a game
    
    Args:
        game_id (str): The game ID
        
    Returns:
        Optional[GameState]: The game state, or None if not found
    """
    return active_games.get(game_id)

def set_current_document(game_id: str, document: Document) -> None:
    """
    Set the current document for a game
    
    Args:
        game_id (str): The game ID
        document (Document): The document to set
    """
    current_documents[game_id] = document

def get_current_document(game_id: str) -> Optional[Document]:
    """
    Get the current document for a game
    
    Args:
        game_id (str): The game ID
        
    Returns:
        Optional[Document]: The current document, or None if not found
    """
    return current_documents.get(game_id)

def update_game_state_after_decision(
    game_id: str, 
    document: Document, 
    decision: str, 
    is_correct: bool, 
    points: int, 
    narrative_update: str
) -> GameState:
    """
    Update game state after a decision is made
    
    Args:
        game_id (str): The game ID
        document (Document): The document that was decided on
        decision (str): The decision that was made (approve/deny)
        is_correct (bool): Whether the decision was correct
        points (int): The points awarded for the decision
        narrative_update (str): The narrative update for the decision
        
    Returns:
        GameState: The updated game state
    """
    game_state = active_games[game_id]
    
    # Update score
    game_state.score += points
    
    # Update trust/corruption based on correctness
    if is_correct:
        game_state.trust = min(100, game_state.trust + 5)
    else:
        # If incorrect and decision was approve (let bad documents through)
        if decision == "approve":
            game_state.corruption = min(100, game_state.corruption + 10)
        # If incorrect and decision was deny (rejected valid documents)
        else:
            game_state.trust = max(0, game_state.trust - 10)
    
    # Add to traveler history
    game_state.traveler_history.append(TravelerRecord(
        document=document,
        decision=decision,
        correct_decision="approve" if document.is_valid else "deny",
        points=points
    ))
    
    # Add to decisions
    game_state.decisions.append(DecisionRecord(
        document_id=document.id,
        decision=decision,
        is_correct=is_correct,
        points=points
    ))
    
    # Add narrative event
    game_state.narrative_events.append(NarrativeEvent(
        day=game_state.day,
        text=narrative_update,
        type="decision"
    ))
    
    # Update game state
    active_games[game_id] = game_state
    
    # Clear current document
    if game_id in current_documents:
        del current_documents[game_id]
    
    return game_state

def advance_day(game_id: str, next_day: int, day_message: str) -> GameState:
    """
    Advance the game to the next day
    
    Args:
        game_id (str): The game ID
        next_day (int): The next day number
        day_message (str): The day message
        
    Returns:
        GameState: The updated game state
    """
    game_state = active_games[game_id]
    
    # Update day
    game_state.day = next_day
    
    # Add day start narrative event
    game_state.narrative_events.append(NarrativeEvent(
        day=next_day,
        text=day_message,
        type="day_start"
    ))
    
    # Add rule changes for this day
    # In a real implementation, this would come from a rules database
    if next_day == 3:
        game_state.rule_changes.append(RuleChange(
            day=next_day,
            description="Additional verification required for travelers from restricted regions.",
            rule_id="restricted_regions"
        ))
    elif next_day == 5:
        game_state.rule_changes.append(RuleChange(
            day=next_day,
            description="All names must match exactly between documents.",
            rule_id="name_match"
        ))
    elif next_day == 8:
        game_state.rule_changes.append(RuleChange(
            day=next_day,
            description="Permits must have been issued within the last 6 months.",
            rule_id="permit_expiry"
        ))
    
    # Update game state
    active_games[game_id] = game_state
    
    return game_state

def end_game(game_id: str, ending_type: str) -> GameState:
    """
    End the game with the specified ending
    
    Args:
        game_id (str): The game ID
        ending_type (str): The type of ending (corrupt/neutral/strict)
        
    Returns:
        GameState: The final game state
    """
    game_state = active_games[game_id]
    
    # Set game over and ending path
    game_state.is_game_over = True
    game_state.ending_path = ending_type
    
    # Update game state
    active_games[game_id] = game_state
    
    return game_state

def save_game(save_id: str, game_state: GameState, timestamp: str) -> None:
    """
    Save a game state
    
    Args:
        save_id (str): The save ID
        game_state (GameState): The game state to save
        timestamp (str): The timestamp of the save
    """
    saved_games[save_id] = game_state
    save_timestamps[save_id] = timestamp

def load_game(save_id: str) -> Optional[GameState]:
    """
    Load a saved game
    
    Args:
        save_id (str): The save ID
        
    Returns:
        Optional[GameState]: The saved game state, or None if not found
    """
    return saved_games.get(save_id)