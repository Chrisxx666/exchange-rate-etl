import schedule
import time
import subprocess
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def job():
    logging.info("Running ETL process...")
    try:
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("ETL process completed successfully")
        else:
            logging.error(f"ETL process failed with return code {result.returncode}")
            logging.error(f"Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Failed to run ETL process: {e}")

# 設定每天 09:00 執行
schedule.every().day.at("09:00").do(job)

# 啟動時運行一次，無需等待到明天
logging.info("Running initial ETL job...")
job()

logging.info("Scheduler started. Waiting for next run at 09:00...")

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        logging.error(f"Scheduler error: {e}")
        time.sleep(60)  # 即使出錯，也繼續運行
