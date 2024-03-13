from dataclasses import dataclass

@dataclass(frozen=True)
class ExecutionStatusResponse:
    feedback: str
    message: str
    continueCheck: bool
    isRejected: bool
    quantity: float
    cashAccountCurrentBalance: float
