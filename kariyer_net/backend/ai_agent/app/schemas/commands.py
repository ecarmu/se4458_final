from pydantic import BaseModel
from typing import Optional, List

class Command(BaseModel):
    type: str  # search, apply, filter, etc.
    parameters: dict
    confidence: float

class ParsedCommand(BaseModel):
    original_message: str
    commands: List[Command]
    intent: str 