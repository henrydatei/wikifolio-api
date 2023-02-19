# wikifolio-api
A Python API-Wrapper for the unofficial wikifolio API

## Usage
- Clone this repo
- Create a new file inside it with the following content (the wikifolio-ID is the name of your wikifolio, e.g. "wf000igb03")
- **Very important suggestion for everbody using this package!** Don't overdo the API calls. The wikifolio team is not stupid, make pauses/delays between EVERY api action, for example a few seconds. Otherwise it is likely that your IP or account gets blocked. Don't abuse this package to "make a full copy" of the wikifolios on our machine. **Only use what you really need!**

```python
from wikifolio import Wikifolio

wf = Wikifolio("email", "password", "wikifolioID")
print(wf.performance_ever)
```

## Current state of functionality
- tested on a wikifolio which is (not yet) investible [19.02.2023], all things except buy_quote/sell_quote succesfully tested. For my purpose limit (and stop-limit) orders are sufficient.

## Features
- Perfomance Indicators (`wf.performance_since_emission`, `wf.performance_ever`, ...)
- Properties (see [#2](https://github.com/henrydatei/wikifolio-api/issues/2))
- Buy and Sell orders (limit order and quote order)

## TODOs
- 2FA (implemented, but needs testing)
- Somebody with an approved wikifolio account should test and report if and how 2FA works (as reported in the issues, real investing/trading requires 2FA)
- provide some Jupyter notebooks to demonstrate proper use of the "key features"
- in the next days some other code contributions will be committed

## Votes / Abstimmungen
- which communication language is preferred?
- DE : quantomas
- ENG : ??
