# wikifolio-api
A Python API-Wrapper for the unofficial wikifolio API

## Usage
- Clone this repo
- Create a new file inside it with the following content
```python
from wikifolio import Wikifolio

api = Wikifolio("email", "password", "wikifolioID")
print(api.getPerformanceEver())
```

## Features
- Perfomance Indicators (getPerformanceSinceEmission(), getPerformanceEver(), ...)
- Limit Buy and Sell orders (quote orders require a websocket connection in the background and I have no idea how to implement them)