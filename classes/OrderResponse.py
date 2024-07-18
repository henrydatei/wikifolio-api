from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class OrderResponse:
    success: bool
    reason: Optional[str] = field(default=None)
    orderGuid: Optional[str] = field(default=None)
    needsTfaReAuth: Optional[bool] = field(default=None)
    needsPasswordReAuth: Optional[bool] = field(default=None)