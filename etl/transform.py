import pandas as pd
import logging

def transform_data(data):
    """
    Transform raw exchange rate JSON data into a clean pandas DataFrame
    將原始 JSON 匯率資料轉換成 pandas DataFrame，便於儲存與分析
    """
    if data is None:
        logging.warning("No data received for transformation. Returning empty DataFrame.")
        return pd.DataFrame()

    rates = data.get("rates", {})
    if not rates:
        logging.warning("No exchange rates found in the data.")
        return pd.DataFrame()

    # 將「幣別匯率」轉成兩欄格式：currency、rate
    df = pd.DataFrame(rates.items(), columns=["currency", "rate"])

    # 加入原始資料中的 base_currency 與日期資訊
    df["base_currency"] = data.get("base", "USD")
    df["date"] = data.get("date", "")

    # 調整欄位順序，讓資料更有邏輯性
    df = df[["base_currency", "date", "currency", "rate"]]

    logging.info(f"Transformed {len(df)} exchange rate records.")
    return df
