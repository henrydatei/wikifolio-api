import requests
from lxml import etree
import json
import typing
from datetime import datetime, timedelta
from dataclasses import dataclass
import websocket
import random
import time

@dataclass(frozen=True)
class OrderResponse:
    success: bool
    reason: str
    orderGuid: str


@dataclass(frozen=True)
class ExecutionStatusResponse:
    feedback: str
    message: str
    continueCheck: bool
    isRejected: bool


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


@dataclass(frozen=True)
class PortfolioUnderlying:
    assetType: str
    name: str
    amount: float


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


class Wikifolio:
    cookie = None
    name = None
    wikifolio_id = None
    rawData = None

    def __init__(self, username: str, password: str, wikifolio_name: str) -> None:
        params = {
            "email": username,
            "password": password,
            "keepLoggedIn": True
        }
        r = requests.post(
            "https://www.wikifolio.com/api/login?country=de&language=de",
            data=params,
        )
        r.raise_for_status()
        self.cookie = r.cookies
        self.name = wikifolio_name
        self._get_wikifolio_id(wikifolio_name)

    def _get_wikifolio_id(self, name: str) -> None:
        r = requests.get(
            "https://www.wikifolio.com/de/de/w/{}".format(name),
            cookies=self.cookie,
        )
        r.raise_for_status()
        html = etree.fromstring(r.text)
        result = json.loads(html.xpath('//*[@id="__NEXT_DATA__"]/text()')[0])
        self.wikifolio_id = result["props"]["pageProps"]["data"]["wikifolio"]["id"]
        self.rawData = result

    def _get_wikifolio_key_figure(self, metric) -> typing.Optional[float]:
        key_figures = self.rawData["props"]["pageProps"]["data"]["keyFigures"]
        return key_figures[metric]["ranking"]["value"]

    @property
    def performance_since_emission(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceSinceEmission")

    @property
    def performance_ever(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceEver")

    @property
    def performance_one_year(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceOneYear")

    @property
    def performance_three_years(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performance3Years")

    @property
    def performance_five_years(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performance5Years")

    @property
    def performance_ytd(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceYTD")

    @property
    def performance_annualized(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceAnnualized")

    @property
    def performance_one_month(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceOneMonth")

    @property
    def performance_six_months(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performance6Months")

    @property
    def performance_intraday(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("performanceIntraday")

    @property
    def max_loss(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("maxLoss")

    @property
    def risk_factor(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("riskFactor")

    @property
    def sharp_ratio(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("sharpRatio")

    def buy_limit(
            self,
            amount: int,
            isin: str,
            limit_price: float,
            valid_until: typing.Optional[str] = None
    ) -> OrderResponse:
        if not valid_until:
            valid_until = datetime.strftime(
                datetime.now() + timedelta(days=1), "%Y-%m-%dT%X.%fZ"
            )
        params = {
            "amount": amount,
            "buysell": "buy",
            "limitPrice": limit_price,
            "orderType": "limit",
            "stopLossLimitPrice": "",
            "stopLossStopPrice": "",
            "stopPrice": 0,
            "takeProfitLimitPrice": "",
            "underlyingIsin": isin,
            "validUntil": valid_until,
            "wikifolioId": self.wikifolio_id,
        }
        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        raw_json = r.json()
        return OrderResponse(**raw_json)

    def sell_limit(
            self,
            amount: int,
            isin: str,
            limit_price: float,
            valid_until: typing.Optional[str] = None
    ) -> OrderResponse:
        if not valid_until:
            valid_until = datetime.strftime(
                datetime.now() + timedelta(days=1), "%Y-%m-%dT%X.%fZ"
            )
        params = {
            "amount": amount,
            "buysell": "sell",
            "limitPrice": limit_price,
            "orderType": "limit",
            "stopLossLimitPrice": "",
            "stopLossStopPrice": "",
            "stopPrice": 0,
            "takeProfitLimitPrice": "",
            "underlyingIsin": isin,
            "validUntil": valid_until,
            "wikifolioId": self.wikifolio_id,
        }
        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        raw_json = r.json()
        return OrderResponse(**raw_json)

    def trade_execution_status(self, order_uuid: str) -> ExecutionStatusResponse:
        params = {
            "order": order_uuid,
        }
        r = requests.get(
            "https://www.wikifolio.com/api/virtualorder/tradeexecutionstatus",
            params=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        raw_json = r.json()
        return ExecutionStatusResponse(**raw_json)

    def search(self, term: str) -> typing.List[SearchResult]:
        params = {
            "term": term,
            "wikifolio": self.wikifolio_id,
        }
        r = requests.post(
            "https://www.wikifolio.com/dynamic/de/de/publish/autocompleteunderlyings",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        raw_json = r.json()
        return [SearchResult(**raw_search_result) for raw_search_result in raw_json]

    def get_content(self) -> Portfolio:
        header = {
            "accept": "application/json",
        }
        params = {
            "includeportfolio": True,
            "country": "de",
            "language": "de",
        }
        r = requests.get(
            "https://www.wikifolio.com/api/chart/{}/data".format(self.wikifolio_id),
            params=params,
            headers=header,
        )
        r.raise_for_status()
        raw_json = r.json()
        portfolio = raw_json["portfolio"]
        return Portfolio(**portfolio)

    def get_trade_history(self, page: int = 0, page_size: int = 10) -> typing.List[Order]:
        header = {
            "accept": "application/json",
        }
        params = {
            "page": page,
            "pagesize": page_size,
            "country": "de",
            "language": "de",
        }
        r = requests.get(
            "https://www.wikifolio.com/api/wikifolio/{}/tradehistory".format(self.wikifolio_id),
            params=params,
            headers=header,
            cookies=self.cookie,
        )
        r.raise_for_status()
        raw_json = r.json()
        orders = raw_json["tradeHistory"]["orders"]
        return [Order(**raw_order) for raw_order in orders]

    def buy_quote(self, amount: int, isin: str) -> OrderResponse:
        params = {
            "clientProtocol": 1.5, 
            "connectionData": [
                {"name":"livehub"},
                {"name":"quotehub"}
            ],
            "_": int(time.time() * 1000),
        }
        r = requests.get(
            "https://www.wikifolio.com/de/de/signalr/negotiate",
            data = params,
            cookies = self.cookie
        )
        r.raise_for_status()
        connection_token = r.json()["ConnectionToken"]
        protocol_version = r.json()["ProtocolVersion"]

        ws = websocket.WebSocket()
        tid = 1 # random.randint(1, 10)
        socket = f'wss://www.wikifolio.com/de/de/signalr/connect?transport=webSockets&clientProtocol={protocol_version}&connectionToken={connection_token}&connectionData=%5B%7B%22name%22%3A%22livehub%22%7D%2C%7B%22name%22%3A%22quotehub%22%7D%5D&tid={tid}'
        ws.connect(socket)

        wiki_id = self.wikifolio_id
        trade_data = {
            'H': "quotehub", 
            'M': "GetQuote", 
            'A': [wiki_id, isin, f"{amount}", 910], #Vorletzte Ziffer Menge; 910 Buy Order, 920 Sell Order
            'I': 1 #Anzahl der x-Anfrage an den Server
            }

        ws.recv_data()
        ws.send(json.dumps(trade_data))

        QuoteId = ws.recv_data()
        print(QuoteId)
        QuoteId = json.loads(QuoteId[1].decode('utf-8'))['M'][0]['A'][0]['QuoteId']
        print(QuoteId)
        ws.close()

        order = {
            'amount': amount,
            'buysell': "buy",
            'limitPrice': "",
            'orderType': "quote",
            'quoteId': QuoteId,
            'stopLossLimitPrice': "",
            'stopLossStopPrice': "",
            'stopPrice': "",
            'takeProfitLimitPrice': "",
            'underlyingIsin': isin,
            'validUntil': "",
            'wikifolioId': wiki_id
            }

        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data = order,
            cookies = self.cookie
        )
        r.raise_for_status()
        return OrderResponse(**r.json())

    def sell_quote(self, amount: int, isin: str) -> OrderResponse:
        params = {
            "clientProtocol": 1.5, 
            "connectionData": [
                {"name":"livehub"},
                {"name":"quotehub"}
            ],
            "_": int(time.time() * 1000),
        }
        r = requests.get(
            "https://www.wikifolio.com/de/de/signalr/negotiate",
            data = params,
            cookies = self.cookie
        )
        r.raise_for_status()
        connection_token = r.json()["ConnectionToken"]
        protocol_version = r.json()["ProtocolVersion"]

        ws = websocket.WebSocket()
        tid = 1 # random.randint(1, 10)
        socket = f'wss://www.wikifolio.com/de/de/signalr/connect?transport=webSockets&clientProtocol={protocol_version}&connectionToken={connection_token}&connectionData=%5B%7B%22name%22%3A%22livehub%22%7D%2C%7B%22name%22%3A%22quotehub%22%7D%5D&tid={tid}'
        ws.connect(socket)

        wiki_id = self.wikifolio_id
        trade_data = {
            'H': "quotehub", 
            'M': "GetQuote", 
            'A': [wiki_id, isin, f"{amount}", 920], #Vorletzte Ziffer Menge; 910 Buy Order, 920 Sell Order
            'I': 1 #Anzahl der x-Anfrage an den Server
            }

        ws.recv_data()
        ws.send(json.dumps(trade_data))

        QuoteId = ws.recv_data()
        print(QuoteId)
        QuoteId = json.loads(QuoteId[1].decode('utf-8'))['M'][0]['A'][0]['QuoteId']
        print(QuoteId)
        ws.close()

        order = {
            'amount': amount,
            'buysell': "sell",
            'limitPrice': "",
            'orderType': "quote",
            'quoteId': QuoteId,
            'stopLossLimitPrice': "",
            'stopLossStopPrice': "",
            'stopPrice': "",
            'takeProfitLimitPrice': "",
            'underlyingIsin': isin,
            'validUntil': "",
            'wikifolioId': wiki_id
            }

        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data = order,
            cookies = self.cookie
        )
        r.raise_for_status()
        return OrderResponse(**r.json())