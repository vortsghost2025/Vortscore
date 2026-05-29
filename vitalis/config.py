from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class CognitionConfig:
    # Deterministic Engine Configuration
    LOGIC_BASED: bool = True
    PLAN_SCHEMA: Dict[str, Any] = field(default_factory=lambda: {
        "type": "object",
        "required": ["intent"]
    })

@dataclass(frozen=True)
class LoggingConfig:
    LOG_LEVEL: str = "INFO"

cognition_cfg = CognitionConfig()
logging_cfg = LoggingConfig()
