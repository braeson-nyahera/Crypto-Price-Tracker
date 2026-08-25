import requests

from .config import FRANKFURTER_RATES_URL, BASE, QUOTES




def transform_data(data):
    params = {"base" : BASE,"quotes": QUOTES}

    rates = requests.get(FRANKFURTER_RATES_URL, params=params, timeout=10)
    rates.raise_for_status()
    rate = rates.json()[0]["rate"]
    for item in data:
        item["USD/KES rates"] = rate
        item["Approx. Price KES"] = float(item["price"]) * rate

    return data