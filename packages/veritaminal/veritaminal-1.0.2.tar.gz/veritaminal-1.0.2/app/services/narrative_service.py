"""
Narrative service for Veritaminal API

Handles story progression, narrative updates, and endings.
"""

from typing import Dict, List, Optional, Tuple
from ..models import Document, GameState
import sys
import os

# Add the game module to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from game import api as game_api
from game import narrative as game_narrative

def generate_update(game_state: GameState, document: Document, decision: str, is_correct: bool) -> str:
    """
    Generate a narrative update based on the player's decision
    
    Args:
        game_state (GameState): The current game state
        document (Document): The document that was decided on
        decision (str): The decision that was made (approve/deny)
        is_correct (bool): Whether the decision was correct
        
    Returns:
        str: A narrative update
    """
    # Create memory context for the narrative update
    memory_context = ""
    if game_state.narrative_events:
        recent_events = game_state.narrative_events[-3:]  # Last 3 narrative events
        memory_context = "Recent events:\n"
        for event in recent_events:
            memory_context += f"- Day {event.day}: {event.text}\n"
    
    # Use the original game's narrative update system
    current_state = {
        "corruption": game_state.corruption,
        "trust": game_state.trust,
        "day": game_state.day
    }
    
    # Generate narrative update
    update = game_api.generate_narrative_update(
        current_state,
        decision,
        is_correct,
        memory_context
    )
    
    return update

def generate_day_message(day: int, game_state: GameState) -> str:
    """
    Generate a message for the start of a new day
    
    Args:
        day (int): The day number
        game_state (GameState): The current game state
        
    Returns:
        str: A day message
    """
    # Generate appropriate message for the day
    setting_name = game_state.border_setting.name
    trust = game_state.trust
    corruption = game_state.corruption
    
    # Define base day messages
    day_messages = {
        1: f"Day 1: Welcome to {setting_name}. Your assignment begins today.",
        2: f"Day 2: Your second day at {setting_name}. The border is busy.",
        3: f"Day 3: New regulations have been implemented due to heightened security concerns.",
        4: f"Day 4: You're starting to get comfortable with your role at {setting_name}.",
        5: f"Day 5: Additional verification protocols are now in effect.",
        6: f"Day 6: Rumors of document forgery rings are circulating.",
        7: f"Day 7: Your superiors are closely monitoring your performance.",
        8: f"Day 8: New permit expiration rules have been implemented.",
        9: f"Day 9: Tensions are high as your assignment nears completion.",
        10: f"Day 10: Your final day at {setting_name}. Make it count."
    }
    
    # Get base message
    message = day_messages.get(day, f"Day {day}: Another day at {setting_name}.")
    
    # Add context based on trust and corruption
    if corruption > 70:
        message += " Your growing connections with smugglers are becoming noticed."
    elif corruption > 40:
        message += " You've developed some questionable relationships at the border."
    
    if trust < 30:
        message += " Your superiors are concerned about your judgment."
    elif trust > 70:
        message += " Your supervisors appreciate your diligence."
    
    return message

def generate_ending(game_state: GameState) -> Tuple[str, str]:
    """
    Generate an ending based on the final game state
    
    Args:
        game_state (GameState): The final game state
        
    Returns:
        Tuple[str, str]: The ending type and ending message
    """
    # Determine ending type based on corruption and trust
    corruption = game_state.corruption
    trust = game_state.trust
    
    if corruption > 70:
        ending_type = "corrupt"
        ending_message = "Your corruption has caught up with you. You've been removed from your post and are under investigation for accepting bribes and aiding criminal networks."
    elif trust < 30:
        ending_type = "strict"
        ending_message = "Your rigid adherence to the rules has made you unpopular. You've been reassigned to a remote outpost where your scrutiny will be less disruptive."
    else:
        ending_type = "neutral"
        ending_message = "You've completed your assignment with a balanced approach. Your superiors recognize your fair judgment and have offered you a promotion."
    
    # Add context based on score
    score = game_state.score
    if score > 200:
        ending_message += " Your exceptional performance has been noted in your permanent record."
    elif score < 0:
        ending_message += " Your poor performance will make future assignments difficult to secure."
    
    return ending_type, ending_message