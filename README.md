# wikifolio-api
A Python API-Wrapper for the unofficial wikifolio API

## Usage
- Clone this repo
- Create a new file inside it with the following content (the wikifolio-ID is the name of your wikifolio, e.g. "wf000igb03")

```python
from wikifolio import Wikifolio

wf = Wikifolio("email", "password", "wikifolioID")
print(wf.performance_ever)
```

## Features
- Perfomance Indicators (`wf.performance_since_emission`, `wf.performance_ever`, ...)
- Buy and Sell orders (Limit order and quote order)

Please note that there are currently some strange things going on when creating quote orders: Not every quote order is successful, so try the order again if it's not working! I'm trying to fix this.

## TODOs
- 2FA
