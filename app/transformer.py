from datetime import datetime, time
def transform_data(data, currency, rate):
    for item in data:
        item['price'] = float(item['price'])
        item[f"USD/{currency} rates"] = rate
        item[f"Approx. Price {currency}"] = round(float((item["price"]) * rate),2)
        item['extracted_at'] = str(datetime.now().replace(microsecond=0))
        round(item['price'],2)

    return data