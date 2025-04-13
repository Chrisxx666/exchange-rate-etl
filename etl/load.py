import os
from sqlalchemy import create_engine


def save_to_csv(df, filename = "exchange_rates.csv"):
    """
    Saves the given DataFrame to a CSV file inside the 'data' directory.
    """
    directory = "data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    df.to_csv(filepath, index = False)
    print(f"CSV saved to {filepath}")

def save_to_mysql(df, db_config, table_name = "exchange_rates"):
    """
    Saves the given DataFrame to a MySQL database table using SQLAlchemy.

    df: pandas DataFrame to be saved
    db_config: a dictionary with host, user, password, database, port
    table_name: name of the MySQL table to write into
    """
    try:
        # 建立連線字串
        connection_str = (
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        )

        # use SQLAlchemy 建立 Engine
        engine = create_engine(connection_str)

        # 將資料寫入資料表（如果表已存在則覆蓋）
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"Data inserted into MySQL table '{table_name}'")

    except Exception as e:
        print(f"Failed to write to MySQL : {e}")
