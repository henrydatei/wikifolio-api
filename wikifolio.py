import requests
from lxml import etree
import json
from datetime import datetime, timedelta


class Wikifolio:
    cookie = None
    name = None
    wikifolio_id = None
    rawData = None

    def __init__(self, username, password, wikifolio_name):
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

    def _get_wikifolio_id(self, name):
        r = requests.get(
            "https://www.wikifolio.com/de/de/w/{}".format(name),
            cookies=self.cookie,
        )
        r.raise_for_status()
        html = etree.fromstring(r.text)
        result = json.loads(html.xpath('//*[@id="__NEXT_DATA__"]/text()')[0])
        self.wikifolio_id = result["props"]["pageProps"]["data"]["wikifolio"]["id"]
        self.rawData = result

    def _get_wikifolio_key_figure(self, metric):
        key_figures = self.rawData["props"]["pageProps"]["data"]["keyFigures"]
        return key_figures[metric]["ranking"]["value"]

    @property
    def performance_since_emission(self):
        return self._get_wikifolio_key_figure("performanceSinceEmission")

    @property
    def performance_ever(self):
        return self._get_wikifolio_key_figure("performanceEver")

    @property
    def performance_one_year(self):
        return self._get_wikifolio_key_figure("performanceOneYear")

    @property
    def performance_three_years(self):
        return self._get_wikifolio_key_figure("performance3Years")

    @property
    def performance_five_years(self):
        return self._get_wikifolio_key_figure("performance5Years")

    @property
    def performance_ytd(self):
        return self._get_wikifolio_key_figure("performanceYTD")

    @property
    def performance_annualized(self):
        return self._get_wikifolio_key_figure("performanceAnnualized")

    @property
    def performance_one_month(self):
        return self._get_wikifolio_key_figure("performanceOneMonth")

    @property
    def performance_six_months(self):
        return self._get_wikifolio_key_figure("performance6Months")

    @property
    def performance_intraday(self):
        return self._get_wikifolio_key_figure("performanceIntraday")

    @property
    def max_loss(self):
        return self._get_wikifolio_key_figure("maxLoss")

    @property
    def risk_factor(self):
        return self._get_wikifolio_key_figure("riskFactor")

    @property
    def sharp_ratio(self):
        return self._get_wikifolio_key_figure("sharpRatio")

    def buy_limit(self, amount, isin, limit_price, valid_until=""):
        if valid_until == "":
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
        return r.json()

    def sell_limit(self, amount, isin, limit_price, valid_until=""):
        if valid_until == "":
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
        return r.json()

    def trade_execution_status(self, order_id):
        params = {
            "order": order_id,
        }
        r = requests.get(
            "https://www.wikifolio.com/api/virtualorder/tradeexecutionstatus",
            params=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        return r.json()

    def search(self, term):
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
        return r.json()

    def get_content(self):
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
        return r.json()

    def get_trade_history(self, page=0, page_size=10):
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
        return r.json()
