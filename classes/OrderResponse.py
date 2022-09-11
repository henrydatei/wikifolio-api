from dataclasses import dataclass

@dataclass(frozen=True)
class OrderResponse:
    success: bool
    reason: str
    orderGuid: str