import os
import time
import logging
import pymysql
from sqlalchemy import create_engine, text


def wait_for_mysql(host, port, user, password, database, retries=15, delay=5):
    """
    等待 MySQL 啟動完成（最多重試 15 次，每次間隔 5 秒）
    """
    logging.info(f"Waiting for MySQL at {host}:{port} to be ready...")

    # 檢查主機是否為 localhost，並在 Docker 環境中自動修正
    if host == 'localhost' and os.environ.get('DB_HOST') == 'mysql':
        logging.warning("Host is set to 'localhost' but DB_HOST is 'mysql'. Using 'mysql' instead.")
        host = 'mysql'

    for attempt in range(retries):
        try:
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connect_timeout=10
            )
            connection.close()
            logging.info(f"MySQL at {host}:{port} is ready!")
            return True
        except pymysql.MySQLError as e:
            logging.warning(f"Attempt {attempt + 1}/{retries} - MySQL not ready: {e}")
            if attempt < retries - 1:
                logging.info(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)

    error_msg = f"MySQL at {host}:{port} did not become ready after {retries} attempts"
    logging.error(error_msg)
    raise Exception(error_msg)

def save_to_csv(df, filename="exchange_rates.csv"):
    """
    將 DataFrame 儲存為 CSV 檔案，放在 data 資料夾
    """
    directory = "data"
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    try:
        df.to_csv(filepath, index=False)
        logging.info(f"CSV file saved to: {filepath}")
    except Exception as e:
        logging.error(f"Failed to save CSV: {e}")


def save_to_mysql(df, db_config, table_name="exchange_rates"):
    """
    將資料儲存到 MySQL，重複日期會先刪除再寫入
    """

    # Debug: 印出目前使用的 DB 連線參數
    logging.info("====== DB CONFIG CHECK ======")
    logging.info(f"DB_HOST: {db_config['host']}")
    logging.info(f"DB_PORT: {db_config['port']}")
    logging.info(f"DB_USER: {db_config['user']}")
    logging.info(f"DB_PASSWORD: {'*' * len(db_config['password'])}")
    logging.info(f"DB_NAME: {db_config['database']}")
    logging.info("====== END CHECK ======")

    try:
        # 等待 MySQL 準備好
        try:
            wait_for_mysql(**db_config)
        except Exception as e:
            logging.error(f"Wait for MySQL failed: {e}")
            # 繼續執行，也許 MySQL 已經準備好了

        # 建立連接字串
        connection_str = (
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        )
        logging.info(
            f"Connecting with: mysql+pymysql://USER:PASS@{db_config['host']}:{db_config['port']}/{db_config['database']}")

        engine = create_engine(connection_str)
        target_date = df["date"].iloc[0]

        with engine.connect() as conn:
            delete_query = text(f"DELETE FROM {table_name} WHERE DATE(date) = :target_date")
            result = conn.execute(delete_query, {"target_date": target_date})
            logging.info(f"Deleted {result.rowcount} rows for date {target_date}")

        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logging.info(f"Data written to MySQL table: {table_name}")

    except Exception as e:
        logging.exception(f"Failed to write to MySQL: {e}")
        raise
