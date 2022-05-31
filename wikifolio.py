import requests
from lxml import etree
import json
from datetime import datetime, timedelta


class Wikifolio:
    cookie = None
    name = None
    wikifolioID = None
    rawData = None

    def __init__(self, username, password, wikifolioName):
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
        self.name = wikifolioName
        self.getWikifolioID(wikifolioName)

    def getWikifolioID(self, name):
        r = requests.get(
            "https://www.wikifolio.com/de/de/w/{}".format(name),
            cookies=self.cookie,
        )
        r.raise_for_status()
        html = etree.fromstring(r.text)
        result = json.loads(html.xpath('//*[@id="__NEXT_DATA__"]/text()')[0])
        self.wikifolioID = result["props"]["pageProps"]["data"]["wikifolio"]["id"]
        self.rawData = result

    def _get_wikifolio_key_figure(self, metric):
        key_figures = self.rawData["props"]["pageProps"]["data"]["keyFigures"]
        return key_figures[metric]["ranking"]["value"]

    def getPerformanceSinceEmission(self):
        return self._get_wikifolio_key_figure("performanceSinceEmission")

    def getPerformanceEver(self):
        return self._get_wikifolio_key_figure("performanceEver")

    def getPerformanceOneYear(self):
        return self._get_wikifolio_key_figure("performanceOneYear")

    def getPerformance3Years(self):
        return self._get_wikifolio_key_figure("performance3Years")

    def getPerformance5Years(self):
        return self._get_wikifolio_key_figure("performance5Years")

    def getPerformanceYTD(self):
        return self._get_wikifolio_key_figure("performanceYTD")

    def getPerformanceAnnualized(self):
        return self._get_wikifolio_key_figure("performanceAnnualized")

    def getPerformanceOneMonth(self):
        return self._get_wikifolio_key_figure("performanceOneMonth")

    def getPerformance6Months(self):
        return self._get_wikifolio_key_figure("performance6Months")

    def getPerformanceIntraday(self):
        return self._get_wikifolio_key_figure("performanceIntraday")

    def getMaxLoss(self):
        return self._get_wikifolio_key_figure("maxLoss")

    def getRiskFactor(self):
        return self._get_wikifolio_key_figure("riskFactor")

    def getSharpRatio(self):
        return self._get_wikifolio_key_figure("sharpRatio")

    def buyLimit(self, amount, isin, limitPrice, validUntil=""):
        if validUntil == "":
            validUntil = datetime.strftime(
                datetime.now() + timedelta(days=1), "%Y-%m-%dT%X.%fZ"
            )
        params = {
            "amount": amount,
            "buysell": "buy",
            "limitPrice": limitPrice,
            "orderType": "limit",
            "stopLossLimitPrice": "",
            "stopLossStopPrice": "",
            "stopPrice": 0,
            "takeProfitLimitPrice": "",
            "underlyingIsin": isin,
            "validUntil": validUntil,
            "wikifolioId": self.wikifolioID,
        }
        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        return r.json()

    def sellLimit(self, amount, isin, limitPrice, validUntil=""):
        if validUntil == "":
            validUntil = datetime.strftime(
                datetime.now() + timedelta(days=1), "%Y-%m-%dT%X.%fZ"
            )
        params = {
            "amount": amount,
            "buysell": "sell",
            "limitPrice": limitPrice,
            "orderType": "limit",
            "stopLossLimitPrice": "",
            "stopLossStopPrice": "",
            "stopPrice": 0,
            "takeProfitLimitPrice": "",
            "underlyingIsin": isin,
            "validUntil": validUntil,
            "wikifolioId": self.wikifolioID,
        }
        r = requests.post(
            "https://www.wikifolio.com/api/virtualorder/placeorder",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        return r.json()

    def tradeExecutionStatus(self, orderID):
        params = {
            "order": orderID,
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
            "wikifolio": self.wikifolioID,
        }
        r = requests.post(
            "https://www.wikifolio.com/dynamic/de/de/publish/autocompleteunderlyings",
            data=params,
            cookies=self.cookie,
        )
        r.raise_for_status()
        return r.json()

    def getContent(self):
        header = {
            "accept": "application/json",
        }
        params = {
            "includeportfolio": True,
            "country": "de",
            "language": "de",
        }
        r = requests.get(
            "https://www.wikifolio.com/api/chart/{}/data".format(self.wikifolioID),
            params=params,
            headers=header,
        )
        r.raise_for_status()
        return r.json()
