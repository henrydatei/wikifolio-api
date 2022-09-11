from dataclasses import dataclass

@dataclass(frozen=True)
class PortfolioUnderlying:
    assetType: str
    name: str
    amount: float