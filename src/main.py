import argparse
import sys
import requests

from pipeline.extract import extract_data
from pipeline.transform import transform_data

def run_pipeline(symbols: list[str]) -> None:
    print(f"[extract]  Fetching prices for {', '.join(symbols)} ...")
    raw = extract_data(symbols)

    transformed_data = transform_data(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Binance ETL pipeline")
    parser.add_argument(
        "--symbol",
        dest="symbols",
        nargs="+",
        default=["BTCUSDT"],
        help="Trading pair(s), e.g. BTCUSDT ETHUSDT",
    )
    # parser.add_argument("--db-url", default=DB_URL, help="SQLAlchemy database URL")
    args = parser.parse_args()

    symbols = [
        symbol.strip().upper()
        for value in args.symbols
        for symbol in value.split(",")
        if symbol.strip()
    ]

    try:
        run_pipeline(symbols)
    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)