import requests

from .config import FRANKFURTER_RATES_URL, BASE




def transform_data(data, currency):
    params = {"base" : BASE,"quotes": currency}

    rates = requests.get(FRANKFURTER_RATES_URL, params=params, timeout=10)
    rates.raise_for_status()
    rate = rates.json()[0]["rate"]
    for item in data:
        item['price'] = round(float(item['price']),2)
        item[f"USD/{currency} rates"] = rate
        item[f"Approx. Price {currency}"] = round(float((item["price"]) * rate),2)

    return data