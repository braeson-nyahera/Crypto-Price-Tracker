import argparse
import sys
import requests

from app.extractor import extract_data
from app.transformer import transform_data
from app.loader import output_data

def run_pipeline(symbols: list[str], output: str, currency: str) -> None:
    crypto_data, rate = extract_data(symbols, currency=currency)

    print("[TRANSFORM]  Enriching extracted data ...")
    transformed_data = transform_data(crypto_data, currency=currency, rate=rate)

    print("[OUTPUT]  Generating output ...")
    output_data(transformed_data, output_form=output, currency=currency)

    



def main() -> None:
    parser = argparse.ArgumentParser(description="Binance ETL pipeline")
    parser.add_argument(
        "--symbol",
        dest="symbols",
        nargs="+",
        default=["BTCUSDT"],
        help="Trading pair(s), e.g. BTCUSDT, ETHUSDT",
        required=True
    )
    parser.add_argument("--output", default="terminal", help="Form of the output e.g json, csv, postgres")
    parser.add_argument("--currency", default="KES", help="Local currency for crypto to be converted to!")
    args = parser.parse_args()

    symbols = [
        symbol.strip().upper()
        for value in args.symbols
        for symbol in value.split(",")
        if symbol.strip()
    ]

    currency = args.currency.strip().upper()
    output_format = args.output.lower()

    try:
        run_pipeline(symbols, output=output_format, currency = currency)
    except requests.exceptions.ConnectionError as e:
        print(f"""
    Network ERROR: Unable to connect to the APIs.
    Please check your internet connection.""")
        sys.exit(1)
    except Exception as e:
        print(f"Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()