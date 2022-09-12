import requests
from lxml import etree
import json
import typing
from datetime import datetime, timedelta
import websocket
import time
from pyotp import TOTP

from classes.ExecutionStatusResponse import ExecutionStatusResponse
from classes.Order import Order
from classes.SearchResult import SearchResult
from classes.OrderResponse import OrderResponse
from classes.Portfolio import Portfolio
from classes.PortfolioUnderlying import PortfolioUnderlying
from classes.Trader import Trader
from classes.PriceInformation import PriceInformation

class Wikifolio:
    cookie = None
    name = None
    wikifolio_id = None
    rawData = None
    twoFA_key = None

    def __init__(self, username: str, password: str, wikifolio_name: str, twoFA_key = None) -> None:
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
        self.twoFA_key = twoFA_key

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

    def _get_wikifolio_data(self, metric):
        key_figures = self.rawData["props"]["pageProps"]["data"]["wikifolio"]
        return key_figures[metric]

    def _get_wikifolio_universes(self, universe, subuniverse) -> typing.Optional[bool]:
        try:
            allowed = not self.rawData["props"]["pageProps"]["data"]["investmentUniverseData"]["universeGroups"][universe]["universes"][subuniverse]["isCrossedOut"]
        except:
            allowed = False
        return allowed

    def _get_wikifolio_master_data(self, metric):
        key_figures = self.rawData["props"]["pageProps"]["data"]["masterData"]
        return key_figures[metric]["value"]

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

    @property
    def ranking_place(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("rankingPlace")

    @property
    def total_investments(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("totalInvestments")

    @property
    def liquidation_figure(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("liquidationFigure")
    
    @property
    def trading_volume(self) -> typing.Optional[float]:
        return self._get_wikifolio_key_figure("tradingVolume")

    @property
    def wikifolio_security_id(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("wikifolioSecurityId")

    @property
    def full_name(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("fullName")

    @property
    def short_description(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("shortDescription")

    @property
    def symbol(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("symbol")

    @property
    def description(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("description")["content"]

    @property
    def status(self) -> typing.Optional[int]:
        return self._get_wikifolio_data("status")

    @property
    def wkn(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("wkn")

    @property
    def is_on_watchlist(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("isOnWatchlist")

    @property
    def is_licensed(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("isLicensed")

    @property
    def is_investable(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("isInvestable")

    @property
    def has_been_investable(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("hasBeenInvestable")

    @property
    def isin(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("isin")

    @property
    def chart_image_url(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("chartImageUrl")

    @property
    def emission_date(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("emissionDate")

    @property
    def daily_fee(self) -> typing.Optional[float]:
        return self._get_wikifolio_data("dailyFee")

    @property
    def performance_fee(self) -> typing.Optional[float]:
        return self._get_wikifolio_data("performanceFee")

    @property
    def intended_investment(self):
        return self._get_wikifolio_data("intendedInvestment")

    @property
    def contains_leverage_products(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("containsLeverageProducts")

    @property
    def exchange_ratio_multiplier(self) -> typing.Optional[float]:
        return self._get_wikifolio_data("exchangeRatioMultiplier")

    @property
    def is_second_isin(self) -> typing.Optional[bool]:
        return self._get_wikifolio_data("isSecondIsin")

    @property
    def currency(self) -> typing.Optional[str]:
        return self._get_wikifolio_data("currency")

    @property
    def trader(self) -> typing.Optional[Trader]:
        return Trader(**self.rawData["props"]["pageProps"]["data"]["trader"])

    @property
    def shares_dax(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(0,0)

    @property
    def shares_sdax(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(0,1)

    @property
    def shares_tecdax(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(0,2)

    @property
    def shares_other(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(0,3)

    @property
    def shares_mdax(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(0,4)

    @property
    def shares_europe_select(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(1,0)

    @property
    def shares_dow_jones(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(2,0)

    @property
    def shares_usa_select(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(2,1)

    @property
    def shares_nasdaq_100_select(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(2,2)

    @property
    def shares_hot_stocks(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(3,0)

    @property
    def shares_easteurope_select(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(4,0)

    @property
    def shares_japan_select(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(4,1)

    @property
    def shares_international(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(4,2)

    @property
    def etf_latin_southamerica(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,0)

    @property
    def etf_emerging_markets(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,1)

    @property
    def etf_coutries_of_europe(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,2)

    @property
    def etf_northamerica(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,3)

    @property
    def etf_other_bonds(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,4)

    @property
    def etf_world(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,5)

    @property
    def etf_commodities_etcs(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,6)

    @property
    def etf_germany(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,7)

    @property
    def etf_countries_other(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,8)

    @property
    def etf_dax(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,9)

    @property
    def etf_induboolies(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,10)

    @property
    def etf_eurostoxx(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,11)

    @property
    def etf_asia(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,12)

    @property
    def etf_europe_bonds(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,13)

    @property
    def etf_europe_complete(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,14)

    @property
    def etf_basic_resources(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,15)

    @property
    def etf_other(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(5,16)

    @property
    def fund_properties(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,0)

    @property
    def fund_bonds(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,1)

    @property
    def fund_shares(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,2)

    @property
    def fund_finance_market(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,3)

    @property
    def fund_dab(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,4)

    @property
    def fund_mix(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(6,5)

    @property
    def discount_certificates(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(7,0)

    @property
    def bonus_certificates(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(7,1)

    @property
    def other_investment_certificates(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(7,2)

    @property
    def knock_out_products(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(8,0)

    @property
    def warrants(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(8,1)

    @property
    def other_leverage_products(self) -> typing.Optional[bool]:
        return self._get_wikifolio_universes(8,2)

    @property
    def creation_date(self) -> typing.Optional[str]:
        return self._get_wikifolio_master_data("creationDate")

    @property
    def index_level(self) -> typing.Optional[str]:
        return self._get_wikifolio_master_data("indexLevel")

    @property
    def high_watermark(self) -> typing.Optional[str]:
        return self._get_wikifolio_master_data("highWatermark")
    
    def get_tags(self) -> typing.List[str]:
        tags = []
        # basics
        for tag in self.rawData["props"]["pageProps"]["data"]["tagsData"]["basics"]:
            tags.append(tag["label"])
        # tradings
        for tag in self.rawData["props"]["pageProps"]["data"]["tagsData"]["tradings"]:
            tags.append(tag["label"])
        # rewards
        for tag in self.rawData["props"]["pageProps"]["data"]["tagsData"]["rewards"]:
            tags.append(tag["label"])
        return tags

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
        while True:
            try:
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

                quoteId = ws.recv_data()
                quoteId = json.loads(quoteId[1].decode('utf-8'))['M'][0]['A'][0]['QuoteId']
                ws.close()

                if self.twoFA_key != None:
                    auth = requests.post('https://www.wikifolio.com/api/totp/verify', data = self.twoFA_key, cookies = self.cookie)
                    cookies = auth.cookies
                else: 
                    cookies = self.cookie

                order = {
                    'amount': amount,
                    'buysell': "buy",
                    'limitPrice': "",
                    'orderType': "quote",
                    'quoteId': quoteId,
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
                    cookies = cookies
                )
                r.raise_for_status()
                return OrderResponse(**r.json())
            except:
                pass

    def sell_quote(self, amount: int, isin: str) -> OrderResponse:
        while True:
            try:
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

                quoteId = ws.recv_data()
                quoteId = json.loads(quoteId[1].decode('utf-8'))['M'][0]['A'][0]['QuoteId']
                ws.close()

                if self.twoFA_key != None:
                    auth = requests.post('https://www.wikifolio.com/api/totp/verify', data = self.twoFA_key, cookies = self.cookie)
                    cookies = auth.cookies
                else: 
                    cookies = self.cookie

                order = {
                    'amount': amount,
                    'buysell': "sell",
                    'limitPrice': "",
                    'orderType': "quote",
                    'quoteId': quoteId,
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
                    cookies = cookies
                )
                r.raise_for_status()
                return OrderResponse(**r.json())
            except:
                pass

    def get_price_information(self) -> PriceInformation:
        headers = {"Accept": "application/json"}
        params = {"country": "de", "language": "de"}
        r = requests.get(
            "https://www.wikifolio.com/api/wikifolio/{}/price".format(self.wikifolio_id),
            params = params,
            headers = headers
        )
        r.raise_for_status()
        return PriceInformation(**r.json())