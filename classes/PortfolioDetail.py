from dataclasses import dataclass

@dataclass(frozen = True)
class PortfolioDetail:
    name: str
    isin: str
    quantity: float
    averagePurchasePrice: float
    ask: float
    bid: float
    close: float
    percentage: float
    link: str
    openLinkInSameTab: bool
    issuer: int
    mid: float
    isLeveraged: bool
    isTicking: bool
    partnerName: str
    isLtsuActive: bool