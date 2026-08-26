import csv
import json
import os.path
from psycopg2 import connect, sql
import sys

from .config import DB_URL


def output_terminal(data, currency):
    if len(data) == 1:
        single_output = f"""
    ------------------------------------------------
    BINANCE CRYPTO DATA
    ------------------------------------------------
    symbol:             {data[0]['symbol']}
    Price USDT:         $ {data[0]['price']:,.2f}
    USD/{currency} Rate:       {data[0][f'USD/{currency} rates']}
    Approx. Price {currency}:  {currency} {data[0][F'Approx. Price {currency}']:,.2f}
    --------------------------------------------------
    Source: Binance
    Status: SUCCESS
    --------------------------------------------------

        """
        print(single_output)

    else:
        print(f"""
    --------------------------------------------------------------------
    SYMBOL       USDT PRICE              APPROXIMATE {currency} (rates = {data[0][f'USD/{currency} rates']})
    --------------------------------------------------------------------""")
        for value in data:
            print(f"    {value['symbol']:<10}   $ {value['price']:<20}  {currency} {value[f'Approx. Price {currency}']:,.2F}")
        print(f"    --------------------------------------------------------------------")  

def output_json(data):
    output_path = os.path.abspath("output.json")
    with open(output_path, "w") as output_file:
        json.dump(data, output_file, indent=2)

    print(f"JSON file successfully created at: {output_path}")

def output_csv(data):
    fieldnames = data[0].keys()
    output_path = os.path.abspath('output.csv')

    with open(output_path, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(data)

    print(f"CSV file successfully created at: {output_path}")

def output_postgres(data, db_url, currency):
    try:
        with connect(db_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS crypto_prices_in_{currency} (
                        id BIGSERIAL PRIMARY KEY,
                        symbol TEXT NOT NULL,
                        price_in_$ NUMERIC(20, 8) NOT NULL,
                        {currency}_exchange_rate NUMERIC(20, 8) NOT NULL,
                        approximate_price_in_{currency} NUMERIC(20, 8) NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
                cursor.executemany(
                    f"""
                    INSERT INTO crypto_prices_in_{currency}
                        (symbol, price_in_$, {currency}_exchange_rate, approximate_price_in_{currency})
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        (
                            item["symbol"],
                            item["price"],
                            item[f"USD/{currency} rates"],
                            item[f"Approx. Price {currency}"],
                        )
                        for item in data
                    ],
                )
        print(f"PostgreSQL output written successfully ({len(data)} rows).")
    except Exception as error:
        print(f"PostgreSQL connection or write failed: {error}",file=sys.stderr)
        sys.exit(1)

def output_data(data, output_form, currency):
    if output_form == "terminal":
        output_terminal(data, currency)
    elif output_form == 'json':
        output_json(data)
    elif output_form == 'csv':
        output_csv(data)
    elif output_form == 'postgres':
        output_postgres(data, db_url = DB_URL, currency=currency)