from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class CheckStatus(Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    INFO = "info"

@dataclass
class CheckResult:
    status: CheckStatus
    name: str
    message: str = ""
    attachment: Optional[tuple[str, str]] = None  # (filename, content)
