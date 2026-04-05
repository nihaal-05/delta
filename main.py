import os
import requests
import time

# Get API keys from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BASE_URL = "https://api.delta.exchange"

def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers/BTCUSD"
        response = requests.get(url)
        data = response.json()
        price = float(data["result"]["last_price"])
        return price
    except Exception as e:
        print("Error fetching price:", e)
        return None


def run_bot():
    while True:
        price = get_btc_price()
        
        if price:
            print(f"BTC Price: {price}")
        else:
            print("Failed to fetch price")

        time.sleep(10)  # run every 10 seconds


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
