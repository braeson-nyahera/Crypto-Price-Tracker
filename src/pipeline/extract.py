import requests

from .config import BINANCE_PRICE_URL

def extract_data(symbol):
    prices = []
    for sym in symbol:
        params = {"symbol": sym}

        response = requests.get(BINANCE_PRICE_URL, params=params, timeout=10)
        response.raise_for_status()

        prices.append(response.json())

    return prices