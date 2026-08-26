import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
FRANKFURTER_RATES_URL = "https://api.frankfurter.dev/v2/rates"

BASE = "USD"

DB_URL = f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'