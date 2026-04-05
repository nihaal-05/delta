import os
import requests
import time

BASE_URL = "https://api.delta.exchange"

def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers"
        response = requests.get(url)
        data = response.json()

        for item in data["result"]:
            if item["symbol"] == "BTCUSD":
                return float(item["last_price"])

        return None

    except Exception as e:
        print("Error fetching BTC price:", e)
        return None


def get_all_options():
    try:
        url = BASE_URL + "/v2/products"
        response = requests.get(url)
        data = response.json()
        return data["result"]
    except Exception as e:
        print("Error fetching products:", e)
        return []


def filter_btc_options(products):
    btc_options = []

    for p in products:
        if p["underlying_asset"] == "BTC" and p["contract_type"] == "option":
            btc_options.append(p)

    return btc_options


def run_bot():
    while True:
        print("\n--- Running Scanner ---")

        btc_price = get_btc_price()
        print(f"BTC Price: {btc_price}")

        products = get_all_options()
        btc_options = filter_btc_options(products)

        print(f"Total BTC Options Found: {len(btc_options)}")

        # Print first 5 options for now
        for opt in btc_options[:5]:
            print(f"{opt['symbol']} | Strike: {opt.get('strike_price')} | Expiry: {opt.get('expiry_date')}")

        time.sleep(15)


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
