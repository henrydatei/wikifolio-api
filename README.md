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

## TODOs
- Limit Buy and Sell orders (quote orders require a websocket connection in the background and I have no idea how to implement them)
