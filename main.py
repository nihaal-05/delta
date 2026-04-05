import requests
import time

BASE_URL = "https://api.delta.exchange"


# 🔹 Get BTC price (FIXED)
def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers"
        response = requests.get(url)
        data = response.json()

        for item in data.get("result", []):
            if item.get("symbol") == ".DEBTCUSDT":
                return float(item.get("mark_price", 0))

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


# 🔹 Filter BTC options
def filter_btc_options(products):
    btc_options = []

    for p in products:
        try:
            contract_type = str(p.get("contract_type", "")).lower()
            underlying_symbol = p.get("underlying_asset", {}).get("symbol", "")

            if "option" in contract_type and underlying_symbol == "BTC":
                btc_options.append(p)

        except:
            continue

    return btc_options


# 🔹 Select ONE best strike (CE or PE)
def select_best_option(options, btc_price):
    closest_option = None
    min_diff = float("inf")

    for opt in options:
        try:
            strike = float(opt.get("strike_price", 0))
            diff = abs(strike - btc_price)

            if diff < min_diff:
                min_diff = diff
                closest_option = opt

        except:
            continue

    return closest_option


# 🔹 Main bot loop
def run_bot():
    while True:
        print("\n--- RUNNING BOT ---")

        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        products = get_all_products()
        btc_options = filter_btc_options(products)

        print("Total BTC Options:", len(btc_options))

        if btc_price and len(btc_options) > 0:
            best_option = select_best_option(btc_options, btc_price)

            if best_option:
                print("\n🎯 SELECTED OPTION:")
                print(
                    f"{best_option.get('symbol')} | Strike: {best_option.get('strike_price')} | Type: {best_option.get('contract_type')}"
                )
        else:
            print("No valid data")

        time.sleep(15)


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
