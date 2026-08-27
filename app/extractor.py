import requests
import sys

from .config import BINANCE_PRICE_URL, FRANKFURTER_RATES_URL, BASE

def extract_crypto_data(symbols):
    try:
        prices = []
        for symbol in symbols:
            params = {"symbol": symbol}

            response = requests.get(BINANCE_PRICE_URL, params=params, timeout=10)
            response.raise_for_status()

            prices.append(response.json())

        return prices
    except requests.exceptions.HTTPError:
            print(f"ERROR: {symbol} is not a valid Binance trading pair.")
            sys.exit(1)


def extract_exchange_rates(currency):
    try:
        params = {"base" : BASE,"quotes": currency}
        
        rates = requests.get(FRANKFURTER_RATES_URL, params=params, timeout=10)
        rates.raise_for_status()
        rate = rates.json()[0]["rate"]

        return rate
    except requests.exceptions.HTTPError:
        print(f"ERROR: Unable to retrieve the USD/{currency} exchange rate.")
        sys.exit(1)

def extract_data(symbols, currency):

    print(f"[EXTRACT]  Fetching prices for {', '.join(symbols)} ...")
    crypto_data = extract_crypto_data(symbols=symbols)

    print(f"[EXTRACT]  Fetching exhange rates for {BASE}/{currency} ...")
    exchange_rate = extract_exchange_rates(currency=currency)
    
    return crypto_data, exchange_rate