import argparse
import sys
import requests

from app.extract import extract_data
from app.transform import transform_data
from app.output import output_data

def run_pipeline(symbols: list[str], output: str, currency: str) -> None:
    print(f"[extract]  Fetching prices for {', '.join(symbols)} ...")
    raw = extract_data(symbols)

    print("[transform]  Enriching extracted data ...")
    transformed_data = transform_data(raw, currency)

    print("[output]  Generating output ...")
    output_data(transformed_data, output_form=output, currency=currency)

    



def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Binance ETL pipeline")
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

    try:
        run_pipeline(symbols, output=args.output, currency = args.currency)
    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()