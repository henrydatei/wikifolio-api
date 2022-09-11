from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class SearchResult:
    Isin: str
    Wkn: str
    ShortDescription: str
    InvestmentUniverse: str
    LongDescrtiption: str
    PartnerLink: str
    SecurityType: int
    IsAvailableInWikifolio: bool
    IsNotAvailableReason: typing.Optional[str]
    Relevance: float
    Issuer: typing.Optional[int]