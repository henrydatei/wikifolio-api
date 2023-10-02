from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class OrderResponse:
    success: bool
    reason: str
    orderGuid: str
    needsTfaReAuth: Optional[bool]
    needsPasswordReAuth: Optional[bool]