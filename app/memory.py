from typing import Dict, List, Any
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class SessionFlags:
    site_visit_status: str = "not_requested"
    site_visit_datetime: str = None
    follow_up_required: bool = False
    follow_up_preferred_time: str = None
    escalated_to_human: bool = False
    escalation_reason: str = None
    do_not_contact: bool = False

@dataclass
class Session:
    session_id: str
    history: List[Dict[str, Any]] = field(default_factory=list)
    flags: SessionFlags = field(default_factory=SessionFlags)

class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
    
    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(session_id=session_id)
        return self._sessions[session_id]
    
    def get(self, session_id: str) -> Session:
        return self._sessions.get(session_id)
    
    def delete(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

store = SessionStore()
