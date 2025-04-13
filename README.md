# Exchange Rate ETL Pipeline

This project implements a complete ETL (Extract, Transform, Load) pipeline in Python. It retrieves real-time exchange rate data from a public API, transforms it into a structured format using pandas, and loads the data into both a MySQL database and a local CSV file.

## Project Structure
exchange-rate-etl/ ├── etl/ │ ├── extract.py │ ├── transform.py │ ├── load.py ├── data/ │ └── exchange_rates.csv ├── main.py ├── requirements.txt ├── schema.sql ├── .gitignore ├── README.md

## Features

- Fetches exchange rate data from https://exchangerate.host
- Transforms JSON response into a structured DataFrame
- Saves the output to:
  - A local CSV file (`data/exchange_rates.csv`)
  - A MySQL table (`exchange_db.exchange_rates`)
- Modular code structure (extract / transform / load)

## Installation

1. Clone this repository and navigate to the project folder.

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate

## MySQL Setup

1. Ensure MySQL Server is installed and running locally.

2. Initialize the database and table by running the following command in your terminal:

```bash
mysql -u root -p < schema.sql
# exchange-rate-etl
