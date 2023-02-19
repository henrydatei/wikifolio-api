
import json

import login

from wikifolio import Wikifolio


wikifolioID = "wf00gk0001"

wf = Wikifolio(login.login_mail, login.login_pw, wikifolioID)


print(wf.performance_since_emission)
print(wf.performance_ever)

print(wf.symbol)
print(wf.description)
print(wf.trader)
print(wf.creation_date)

print(wf.get_price_information())

wf.get_tags()

wf.get_content().underlyings


## Trades

trades = wf.get_trade_history()

for a in trades:
    a.name
    a.isin
    a.link
    a.orderType
    a.executionPrice
    a.executionDate
    a.performance
    a.weightage
    print('---')


## Portfolio

portf = wf.get_portfolio()

print(json.dumps(portf, indent = 2))

print(json.dumps(portf['groups'][1], indent = 2))

