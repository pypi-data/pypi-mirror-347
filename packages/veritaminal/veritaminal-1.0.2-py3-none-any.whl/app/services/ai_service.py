"""
AI service for Veritaminal API

Handles AI-powered document judgment and hint generation.
"""

from typing import Dict, List, Optional
from ..models import Document, GameState, AIJudgment
import sys
import os

# Add the game module to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from game import api as game_api

def judge_document(document: Document, game_state: GameState) -> AIJudgment:
    """
    Use AI to judge whether a document should be approved or denied
    
    Args:
        document (Document): The document to judge
        game_state (GameState): The current game state
        
    Returns:
        AIJudgment: The AI's judgment
    """
    # Create context for AI judgment
    setting_context = f"""
    Border Setting: {game_state.border_setting.name}
    Situation: {game_state.border_setting.situation}
    Current Day: {game_state.day}
    """
    
    # Create memory context for AI judgment
    memory_context = ""
    if game_state.traveler_history:
        recent_travelers = game_state.traveler_history[-3:]  # Last 3 travelers
        memory_context = "Recent travelers:\n"
        for traveler in recent_travelers:
            memory_context += f"- {traveler.document.name}: {traveler.decision} (correct: {traveler.correct_decision})\n"
    
    # Get active rules based on current day
    active_rules = [rule.description for rule in game_state.rule_changes if rule.day <= game_state.day]
    setting_context += f"\nActive Rules:\n" + "\n".join([f"- {rule}" for rule in active_rules])
    
    # Use the original game's AI judgment
    judgment_dict = game_api.ai_judge_document(
        {
            "name": document.name,
            "permit": document.permit,
            "backstory": document.backstory,
            **document.additional_fields
        },
        setting_context,
        memory_context
    )
    
    # Convert the judgment dict to our API model
    judgment = AIJudgment(
        decision=judgment_dict.get("decision", "deny"),
        confidence=judgment_dict.get("confidence", 0.5),
        reasoning=judgment_dict.get("reasoning", "Based on standard verification protocols."),
        suspicious_elements=judgment_dict.get("suspicious_elements", [])
    )
    
    return judgment

def generate_hint(document: Document, game_state: GameState) -> str:
    """
    Generate a hint for the player about a document
    
    Args:
        document (Document): The document to generate a hint for
        game_state (GameState): The current game state
        
    Returns:
        str: A hint about the document
    """
    # Create memory context for the hint
    memory_context = f"""
    Border Setting: {game_state.border_setting.name}
    Current Day: {game_state.day}
    Rules in effect:
    """
    
    for rule in game_state.rule_changes:
        if rule.day <= game_state.day:
            memory_context += f"- {rule.description}\n"
    
    # Use the original game's Veritas hint system
    hint = game_api.get_veritas_hint(
        {
            "name": document.name,
            "permit": document.permit,
            "backstory": document.backstory,
            **document.additional_fields
        },
        memory_context,
        system_type="veritas_assistant"
    )
    
    return hint