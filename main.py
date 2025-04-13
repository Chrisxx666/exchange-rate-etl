from etl.extract import fetch_exchange_rates
from etl.transform import transform_data
from etl.load import save_to_csv, save_to_mysql

def main():
    # Step 1: Extract
    raw_data = fetch_exchange_rates()

    # Step 2: Transform
    transformed_data = transform_data(raw_data)

    # Step 3: Save to CSV
    save_to_csv(transformed_data)

    # Step 4: Save to MySQL
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Changyu1995!',
        'database': 'exchange_db',
        'port': 3306
    }

    save_to_mysql(transformed_data, db_config)

if __name__ == "__main__":
    main()
