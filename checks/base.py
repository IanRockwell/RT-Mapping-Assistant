from dataclasses import dataclass
from enum import Enum

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
