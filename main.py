 import requests
import time

BASE_URL = "https://api.delta.exchange"

# Get BTC price
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


# Get all products
def get_all_products():
    try:
        url = BASE_URL + "/v2/products"
        response = requests.get(url)
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print("Error fetching products:", e)
        return []


# Filter BTC options (SAFE VERSION)
def filter_btc_options(products):
    btc_options = []

    for p in products:
        try:
            contract_type = str(p.get("contract_type", "")).lower()
            underlying = str(p.get("underlying", "")).upper()

            # Check option type safely
            if "option" in contract_type and underlying == "BTC":
                btc_options.append(p)

        except Exception as e:
            continue

    return btc_options


def run_bot():
    while True:
        print("\n--- RUNNING SCANNER ---")

        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        products = get_all_products()
        print("Total products:", len(products))

        btc_options = filter_btc_options(products)
        print("BTC Options Found:", len(btc_options))

        # If still 0 → debug automatically
        if len(btc_options) == 0:
            print("\nDEBUG SAMPLE PRODUCT:")
            for p in products[:3]:
                print(p)

        else:
            print("\nSample Options:")
            for opt in btc_options[:5]:
                print(
                    f"{opt.get('symbol')} | Strike: {opt.get('strike_price')} | Expiry: {opt.get('expiry_date')} | Type: {opt.get('contract_type')}"
                )

        time.sleep(15)


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
