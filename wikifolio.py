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
        params = {"email": username, "password": password, "keepLoggedIn": True}
        r = requests.post("https://www.wikifolio.com/api/login?country=de&language=de", data = params)
        r.raise_for_status()
        self.cookie = r.cookies
        self.name = wikifolioName
        self.getWikifolioID(wikifolioName)

    def getWikifolioID(self, name):
        r = requests.get("https://www.wikifolio.com/de/de/w/{}".format(name), cookies = self.cookie)
        r.raise_for_status()
        html = etree.fromstring(r.text)
        result = json.loads(html.xpath('//*[@id="__NEXT_DATA__"]/text()')[0])
        self.wikifolioID = result["props"]["pageProps"]["data"]["wikifolio"]["id"]
        self.rawData = result

    def getPerformanceSinceEmission(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceSinceEmission"]["ranking"]["value"]

    def getPerformanceEver(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceEver"]["ranking"]["value"]

    def getPerformanceOneYear(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceOneYear"]["ranking"]["value"]

    def getPerformance3Years(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performance3Years"]["ranking"]["value"]

    def getPerformance5Years(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performance5Years"]["ranking"]["value"]

    def getPerformanceYTD(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceYTD"]["ranking"]["value"]

    def getPerformanceAnnualized(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceAnnualized"]["ranking"]["value"]

    def getPerformanceOneMonth(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceOneMonth"]["ranking"]["value"]

    def getPerformance6Months(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performance6Months"]["ranking"]["value"]

    def getPerformanceIntraday(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["performanceIntraday"]["ranking"]["value"]

    def getMaxLoss(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["maxLoss"]["ranking"]["value"]

    def getRiskFactor(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["riskFactor"]["ranking"]["value"]

    def getSharpRatio(self):
        return self.rawData["props"]["pageProps"]["data"]["keyFigures"]["sharpRatio"]["ranking"]["value"]

    def buyLimit(self, amount, isin, limitPrice, validUntil = ""):
        if validUntil == "":
            validUntil = datetime.strftime(datetime.now() + timedelta(days = 1), "%Y-%m-%dT%X.%fZ")
        params = {"amount": amount, "buysell": "buy", "limitPrice": limitPrice, "orderType": "limit", "stopLossLimitPrice": "", "stopLossStopPrice": "", "stopPrice": 0, "takeProfitLimitPrice": "", "underlyingIsin": isin, "validUntil": validUntil, "wikifolioId": self.wikifolioID}
        r = requests.post("https://www.wikifolio.com/api/virtualorder/placeorder", data = params, cookies = self.cookie)
        r.raise_for_status()
        if r.json["success"]:
            return r.json["orderGuid"]
        else:
            return r.json()

    def sellLimit(self, amount, isin, limitPrice, validUntil = ""):
        if validUntil == "":
            validUntil = datetime.strftime(datetime.now() + timedelta(days = 1), "%Y-%m-%dT%X.%fZ")
        params = {"amount": amount, "buysell": "sell", "limitPrice": limitPrice, "orderType": "limit", "stopLossLimitPrice": "", "stopLossStopPrice": "", "stopPrice": 0, "takeProfitLimitPrice": "", "underlyingIsin": isin, "validUntil": validUntil, "wikifolioId": self.wikifolioID}
        r = requests.post("https://www.wikifolio.com/api/virtualorder/placeorder", data = params, cookies = self.cookie)
        r.raise_for_status()
        if r.json["success"]:
            return r.json["orderGuid"]
        else:
            return r.json()

    def tradeExecutionStatus(self, orderID):
        params = {"order": orderID}
        r = requests.get("https://www.wikifolio.com/api/virtualorder/tradeexecutionstatus", params = params, cookies = self.cookie)
        r.raise_for_status()
        return r.json()