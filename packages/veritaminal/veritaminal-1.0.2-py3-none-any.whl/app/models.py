"""
Pydantic models for the Veritaminal API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SessionData(BaseModel):
    """Session data for API authentication"""
    session_id: str
    api_key: str
    
class Document(BaseModel):
    """Document model representing traveler documents"""
    id: str
    name: str
    permit: str
    backstory: str
    additional_fields: Dict[str, Any]
    is_valid: Optional[bool] = None

class TravelerRecord(BaseModel):
    """Record of a traveler's border crossing attempt"""
    document: Document
    decision: str
    correct_decision: str
    points: int

class DecisionRecord(BaseModel):
    """Record of a player's decision"""
    document_id: str
    decision: str
    is_correct: bool
    points: int

class NarrativeEvent(BaseModel):
    """Narrative event model"""
    day: int
    text: str
    type: str

class RuleChange(BaseModel):
    """Rule change model"""
    day: int
    description: str
    rule_id: str

class BorderSetting(BaseModel):
    """Border setting model"""
    id: str
    name: str
    description: str
    situation: str
    document_requirements: List[str]
    common_issues: List[str]

class GameState(BaseModel):
    """Game state model"""
    day: int
    corruption: int
    trust: int
    score: int
    traveler_history: List[TravelerRecord]
    decisions: List[DecisionRecord]
    narrative_events: List[NarrativeEvent]
    rule_changes: List[RuleChange]
    ending_path: Optional[str] = None
    is_game_over: bool = False
    border_setting: BorderSetting

class AIJudgment(BaseModel):
    """AI judgment model for document validation"""
    decision: str
    confidence: float
    reasoning: str
    suspicious_elements: List[str]

# Request/Response Models
class InitializeRequest(BaseModel):
    """Request model for initializing API session"""
    api_key: str

class InitializeResponse(BaseModel):
    """Response model for initializing API session"""
    status: str
    session_id: str

class StartGameRequest(BaseModel):
    """Request model for starting a new game"""
    setting_id: str

class StartGameResponse(BaseModel):
    """Response model for starting a new game"""
    game_id: str
    setting: BorderSetting
    day: int

class SaveGameRequest(BaseModel):
    """Request model for saving a game"""
    game_id: str
    game_state: GameState

class SaveGameResponse(BaseModel):
    """Response model for saving a game"""
    save_id: str
    timestamp: str

class LoadGameResponse(BaseModel):
    """Response model for loading a game"""
    game_state: GameState

class SettingsResponse(BaseModel):
    """Response model for getting available border settings"""
    settings: List[BorderSetting]

class DocumentRequest(BaseModel):
    """Request model for generating a document"""
    game_id: str

class DocumentResponse(BaseModel):
    """Response model for document generation"""
    document: Document
    ai_judgment: AIJudgment

class DecisionRequest(BaseModel):
    """Request model for making a decision"""
    game_id: str
    document_id: str
    decision: str

class DecisionResponse(BaseModel):
    """Response model for decision outcome"""
    is_correct: bool
    points: int
    narrative_update: str
    game_state: GameState

class HintRequest(BaseModel):
    """Request model for requesting a hint"""
    game_id: str
    document_id: str

class HintResponse(BaseModel):
    """Response model for hint"""
    hint: str

class NextDayRequest(BaseModel):
    """Request model for advancing to the next day"""
    game_id: str

class NextDayResponse(BaseModel):
    """Response model for advancing to the next day"""
    day: int
    day_message: str
    is_game_over: bool
    ending_type: Optional[str] = None
    ending_message: Optional[str] = None