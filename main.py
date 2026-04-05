 import requests
import time

BASE_URL = "https://api.delta.exchange"


# 🔹 Get BTC price
def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers"
        response = requests.get(url)
        data = response.json()

        for item in data.get("result", []):
            if item.get("symbol") == "BTCUSD":
                return float(item.get("last_price", 0))

        return None

    except Exception as e:
        print("Error fetching BTC price:", e)
        return None


# 🔹 Get all products
def get_all_products():
    try:
        url = BASE_URL + "/v2/products"
        response = requests.get(url)
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print("Error fetching products:", e)
        return []


# 🔹 Filter ONLY BTC options (FIXED)
def filter_btc_options(products):
    btc_options = []

    for p in products:
        try:
            contract_type = str(p.get("contract_type", "")).lower()

            underlying_data = p.get("underlying_asset", {})
            underlying_symbol = underlying_data.get("symbol", "")

            # Correct filter
            if "option" in contract_type and underlying_symbol == "BTC":
                btc_options.append(p)

        except:
            continue

    return btc_options


# 🔹 Main bot loop
def run_bot():
    while True:
        print("\n--- RUNNING SCANNER ---")

        # BTC Price
        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        # Get products
        products = get_all_products()
        print("Total products:", len(products))

        # Filter BTC options
        btc_options = filter_btc_options(products)
        print("BTC Options Found:", len(btc_options))

        # Print results
        if len(btc_options) == 0:
            print("\n⚠️ No BTC options found. Debug sample:")
            for p in products[:3]:
                print(p)
        else:
            print("\nSample BTC Options:")
            for opt in btc_options[:5]:
                print(
                    f"{opt.get('symbol')} | Strike: {opt.get('strike_price')} | Expiry: {opt.get('settlement_time')} | Type: {opt.get('contract_type')}"
                )

        time.sleep(15)


# 🔹 Start bot
if __name__ == "__main__":
    print("Bot started...")
    run_bot()
