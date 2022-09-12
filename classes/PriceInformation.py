from dataclasses import dataclass

@dataclass(frozen = True)
class PriceInformation:
    id: str
    ask: float
    bid: float
    quantityLimitBid: int
    quantityLimitAsk: int
    calculationDate: str
    validUntilDate: str
    wikifolioId: str
    isin: str
    instrument: str
    midPrice: float
    showMidPrice: bool
    currency: str
    isCurrencyConverted: bool
    isTicking: bool