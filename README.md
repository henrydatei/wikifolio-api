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
- Buy and Sell orders (limit order and quote order)

## TODOs
- 2FA
