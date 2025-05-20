from etl.extract import fetch_exchange_rates
from etl.transform import transform_data
from etl.load import save_to_csv, save_to_mysql
import logging
import os
import time  # 添加這一行來導入 time 模塊
from dotenv import load_dotenv

# 優先載入本地 .env，如果不存在就讀 .env.docker
if os.path.exists(".env"):
    load_dotenv(".env")
else:
    load_dotenv(".env.docker")


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("ETL process started.")

    # 在 Docker 環境中，給 MySQL 更多時間啟動
    db_host = os.environ.get("DB_HOST", "")
    logging.info(f"DB_HOST from environment: {db_host}")

    if db_host == "mysql":
        logging.info("Docker environment detected. Waiting for MySQL to start...")
        time.sleep(20)  # 在 Docker 環境中等待更長時間

    # 印出目前讀到的環境變數（用來除錯）
    print("====== ENV VAR CHECK ======")
    print("DB_HOST:", os.getenv("DB_HOST", "未設置"))
    print("DB_PORT:", os.getenv("DB_PORT", "未設置"))
    print("DB_USER:", os.getenv("DB_USER", "未設置"))
    print("DB_NAME:", os.getenv("DB_NAME", "未設置"))
    print("====== END CHECK ======")

    try:
        # 確保 DB_HOST 非空
        if not os.environ.get("DB_HOST"):
            logging.warning("DB_HOST is not set! Using 'mysql' as default.")
            os.environ["DB_HOST"] = "mysql"

        # Step 1: Extract
        raw_data = fetch_exchange_rates()
        if not raw_data:
            logging.error("No data fetched. Exiting ETL process.")
            return

        # Step 2: Transform
        transformed_data = transform_data(raw_data)

        # Step 3a: Save to CSV
        save_to_csv(transformed_data)

        # Step 3b: Save to MySQL
        db_config = {
            "host": os.environ["DB_HOST"],
            "port": int(os.environ["DB_PORT"]),
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "database": os.environ["DB_NAME"]
        }

        logging.info(f"Connecting to MySQL with config: {db_config}")
        save_to_mysql(transformed_data, db_config)

        logging.info("ETL process completed successfully.")

    except Exception as e:
        logging.exception("ETL process failed.")


if __name__ == "__main__":  # 修正這一行，使用雙下劃線
    main()