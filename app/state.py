import asyncio
from typing import Dict, List, Optional, Set
from pydantic import BaseModel


class Team(BaseModel):
    name: str


class SessionState(BaseModel):
    session_id: str
    question_idx: int = 0
    total_questions: int = 10
    open_for_buzz: bool = False
    buzz_order: List[str] = []
    turn_index: int = 0
    answered_correctly: Optional[str] = None
    teams: Dict[str, Team] = {}


class RuntimeSession:
    def __init__(self, state: SessionState):
        self.state = state
        self.host_conns: Set = set()
        self.player_conns: Set = set()
        self.lock = asyncio.Lock()


# In-memory storage
_sessions: Dict[str, RuntimeSession] = {}


async def get_or_create(session_id: str) -> RuntimeSession:
    if session_id not in _sessions:
        _sessions[session_id] = RuntimeSession(SessionState(session_id=session_id))
    return _sessions[session_id]
