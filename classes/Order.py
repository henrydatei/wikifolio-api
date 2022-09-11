from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class Order:
    id: str
    name: str
    isin: str
    link: str
    openLinkInSameTab: bool
    isMainOrder: bool
    mainOrderId: str
    subOrders: typing.List["Order"]
    orderType: str
    issuer: int
    securityType: int
    executionPrice: float
    executionDate: str # TODO should be datetime '2022-05-31T22:16:35+02:00'
    performance: float
    weightage: float
    investmentUniverseGroupId: str
    isLeveraged: bool
    linkParameter: str
    corporateActionType: str
    underlyingConcerned: str
    cash: str