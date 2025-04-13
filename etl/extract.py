import requests

def fetch_exchange_rates():
    """
    Fetches real-time exchange rate data from ExchangeRate-API.
    Returns JSON response if successful, otherwise returns None.
    從ExchangeRate-API取得即時匯率資料, 成功傳回JSON回應, 沒有 None.
    """
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url, timeout = 10)
        # 發送請求給API設定 timeout=10 避免程式卡住
        response.raise_for_status()
        # 如果API有問題（404、403 等）會讓我們主動得知錯誤
        return response.json()
        # 成功則回傳JSON(dict)
    except requests.RequestException as error:
        print("Error fetching exchange rate data", error)
        # 發生錯誤印出錯誤訊息
        return None
        # 當API擷取失敗，我們用 None 做為後續判斷依據（讓 transform 可以接手處理）