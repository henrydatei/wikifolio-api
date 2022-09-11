from dataclasses import dataclass
import typing
from .PortfolioUnderlying import PortfolioUnderlying

@dataclass(init=False, frozen=True)
class Portfolio:
    isSuperWikifolio: bool
    hasWeighting: bool
    underlyings: typing.List[PortfolioUnderlying]

    def __init__(self, isSuperWikifolio, hasWeighting, underlyings):
        object.__setattr__(self, "isSuperWikifolio", isSuperWikifolio)
        object.__setattr__(self, "hasWeighting", hasWeighting)
        object.__setattr__(self, "underlyings", [
            PortfolioUnderlying(**underlying) for underlying in underlyings
        ])