from datetime import datetime, timezone
from typing import Optional, Dict

class LogEntry:
    def __init__(self, level: str, message: str, context: Optional[Dict] = None):
        self.timestamp = datetime.now(timezone.utc).isoformat() + "Z"
        self.level = level
        self.message = message
        self.context = context or {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "context": self.context,
        }
