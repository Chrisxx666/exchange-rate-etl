import pandas as pd

def  transform_data(data):
    """
    Transform raw exchange rate JSON data into clean pandas DataFrame
    """
    if data is None:
        # Return an empty DataFrame if no data was received
        return pd.DataFrame()

    rates = data.get("rates", {})
    # 從 JSON 中取出「幣別匯率」的 dict{}
    # Get the "rates" dictionary from the JSON data

    df = pd.DataFrame(rates.items(), columns = ["currency", "rate"])
    # 把 dict 轉為二欄 DataFrame：貨幣代碼 + 匯率
    # Convert the rates dict into a DataFrame with two columns

    # Add two extra columns: base currency and date
    df["base_currency"] = data.get("base", "USD") # 加入匯率的基準貨幣（USD）
    df["date"] = data.get("date", "") # 加入日期欄位（追蹤匯率是哪一天的）

    return df