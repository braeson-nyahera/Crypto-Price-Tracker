# Crypto Price Tracker

A command-line **ETL pipeline** that fetches live cryptocurrency prices from **Binance**, converts them into a local currency using real-time exchange rates, and delivers the results to your terminal, a JSON file, a CSV file, or a PostgreSQL database.

The project follows a clean **Extract → Transform → Load** architecture and ships with Docker support for a one-command run against a bundled Postgres instance.

---

## Features

- Fetch live prices for one or many Binance trading pairs (e.g. `BTCUSDT`, `ETHUSDT`) in a single run.
- Convert USD-denominated prices into any supported currency (default: **KES**) using live USD→currency exchange rates.
- Four interchangeable output targets: **terminal**, **JSON**, **CSV**, or **PostgreSQL**.
- Timestamps every record for traceability.
- Graceful error handling for invalid trading pairs, unavailable exchange rates, and network failures.
- Containerised with Docker and Docker Compose (app + Postgres 18).
- Fast, reproducible dependency management with [`uv`](https://github.com/astral-sh/uv)

---

## How It Works

The pipeline is split into three stages, each in its own module under `app/`:

1. **Extract** (`app/extractor.py`)
   - Pulls the latest price for each requested symbol from the Binance `ticker/price` endpoint.
   - Pulls the current USD→target-currency exchange rate from the Frankfurter API.

2. **Transform** (`app/transformer.py`)
   - Casts the price to a float.
   - Attaches the exchange rate and computes the approximate price in the local currency.
   - Adds a timestamp to each record.

3. **Load** (`app/loader.py`)
   - Routes the transformed records to the chosen output format (terminal, JSON, CSV, or Postgres).

`main.py` wires these stages together and provides the command-line interface.

---

## Project Structure

```
Crypto-Price-Tracker/
├── app/
│   ├── __init__.py
│   ├── config.py        
│   ├── extractor.py     # Extract: Binance prices + FX rates
│   ├── transformer.py   # Transform: enrich and convert records
│   └── loader.py        # Load: terminal / JSON / CSV / Postgres
├── main.py              # CLI entry point + pipeline orchestration
├── Dockerfile
├── docker-compose.yml   # App + PostgreSQL 18 service
├── pyproject.toml
├── uv.lock
├── .python-version     
└── README.md
```

---

## Requirements

- **Python 3.10+**
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`
- A running **PostgreSQL** instance — only if you use the `postgres` output
- Internet access (the pipeline calls the Binance and Frankfurter APIs)

**Dependencies** (declared in `pyproject.toml`):

- `requests` — HTTP calls to the Binance and Frankfurter APIs
- `psycopg2-binary` — PostgreSQL driver
- `python-dotenv` — loads database credentials from a `.env` file

---

## Installation

Clone the repository:

```bash
git clone https://github.com/braeson-nyahera/Crypto-Price-Tracker.git
cd Crypto-Price-Tracker
```

Install dependencies with `uv` (creates the virtual environment and syncs from the lockfile):

```bash
uv sync
```

---

## Configuration

Database credentials are read from environment variables (loaded from a `.env` file via `python-dotenv`). This is **only required for the `postgres` output**.

Create a `.env` file in the project root:

```env
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

These values are assembled into a connection string in `app/config.py`:

```
postgresql://<DB_USERNAME>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```

> **Note:** `.env`, along with generated `*.json` and `*.csv` files, is git-ignored.

---

## Usage

Run the pipeline with `uv` (the project registers a `price-tracker` script):

```bash
uv run price-tracker --symbol BTCUSDT
```

### Command-line arguments

| Argument     | Required | Default    | Description                                                        |
| ------------ | -------- | ---------- | ------------------------------------------------------------------ |
| `--symbol`   | Yes      | —          | One or more Binance trading pairs (space- or comma-separated).     |
| `--output`   | No       | `terminal` | Output format: `terminal`, `json`, `csv`, or `postgres`.           |
| `--currency` | No       | `KES`      | Local fiat currency to convert prices into (e.g. `KES`, `EUR`).    |

### Examples

Single symbol, printed to the terminal:

```bash
uv run price-tracker --symbol BTCUSDT
```

Multiple symbols at once:

```bash
uv run price-tracker --symbol BTCUSDT ETHUSDT SOLUSDT
```

Convert to Euros and export to CSV:

```bash
uv run price-tracker --symbol BTCUSDT --currency EUR --output csv
```

Write to a PostgreSQL database:

```bash
uv run price-tracker --symbol BTCUSDT ETHUSDT --output postgres
```

---

## Output Formats

- **`terminal`** — prints a formatted summary. A single symbol produces a detailed card; multiple symbols produce a compact table.
- **`json`** — writes `output.json` to the current working directory.
- **`csv`** — writes `output.csv` to the current working directory.
- **`postgres`** — creates the table `crypto_prices_in_<currency>` (if it does not exist) and inserts the records.

### PostgreSQL schema

For each currency, a table named `crypto_prices_in_<currency>` (e.g. `crypto_prices_in_KES`) is created with the following columns:

| Column                            | Type            | Description                                |
| --------------------------------- | --------------- | ------------------------------------------ |
| `id`                              | `BIGSERIAL` PK  | Auto-incrementing identifier.              |
| `symbol`                          | `TEXT`          | Binance trading pair (e.g. `BTCUSDT`).     |
| `price_in_$`                      | `NUMERIC(20,8)` | Price in USD/USDT.                         |
| `<currency>_exchange_rate`        | `NUMERIC(20,8)` | USD→local-currency rate used.              |
| `approximate_price_in_<currency>` | `NUMERIC(20,8)` | Converted price in the local currency.     |
| `extracted_at`                    | `TIMESTAMP`     | When the record was extracted.             |

---

## Running with Docker

The included `docker-compose.yml` builds the app and starts a PostgreSQL 18 database, then runs the pipeline against it automatically.

```bash
docker compose up --build
```

By default, the Compose file runs:

```
--symbol BTCUSDT --output postgres
```

and wires the app to the bundled database (no `.env` file needed — credentials are set directly in the Compose environment). The Postgres service is exposed on host port **5433** (mapped to the container's `5432`).

To change what runs, edit the `command` under the `app` service in `docker-compose.yml`.

---

## APIs Used

- **[Binance API](https://binance-docs.github.io/apidocs/)** — `GET /api/v3/ticker/price` for live symbol prices.
- **[Frankfurter API](https://frankfurter.dev/)** — USD→currency exchange rates.

---

## Error Handling

The pipeline exits with a clear message when:

- A trading pair is not valid on Binance.
- The USD→currency exchange rate cannot be retrieved.
- There is no network connection to the APIs.
- A PostgreSQL connection or write fails.

---

## License
