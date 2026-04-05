import requests
import time

BASE_URL = "https://api.delta.exchange"


# 🔹 Get BTC price (ROBUST)
def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers"
        response = requests.get(url)
        data = response.json()

        for item in data.get("result", []):
            symbol = item.get("symbol", "")

            # pick active BTC market with real price
            if "BTC" in symbol and float(item.get("mark_price", 0)) > 0:
                return float(item.get("mark_price"))

        return None

    except Exception as e:
        print("Error BTC price:", e)
        return None


# 🔹 Get all products
def get_all_products():
    try:
        url = BASE_URL + "/v2/products"
        response = requests.get(url)
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print("Error products:", e)
        return []


# 🔹 Filter BTC options
def filter_btc_options(products):
    result = []

    for p in products:
        try:
            contract_type = str(p.get("contract_type", "")).lower()
            underlying = p.get("underlying_asset", {}).get("symbol", "")

            if "option" in contract_type and underlying == "BTC":
                result.append(p)

        except:
            continue

    return result


# 🔹 Get nearest expiry options
def get_nearest_expiry(options):
    try:
        # sort by expiry
        options = sorted(options, key=lambda x: x.get("settlement_time", ""))
        nearest_time = options[0].get("settlement_time")

        return [opt for opt in options if opt.get("settlement_time") == nearest_time]

    except:
        return []


# 🔹 Select ONE best option (closest strike)
def select_best_option(options, btc_price):
    best = None
    min_diff = float("inf")

    for opt in options:
        try:
            strike = float(opt.get("strike_price", 0))
            diff = abs(strike - btc_price)

            if diff < min_diff:
                min_diff = diff
                best = opt

        except:
            continue

    return best


# 🔹 MAIN LOOP
def run_bot():
    while True:
        print("\n--- BOT RUNNING ---")

        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        products = get_all_products()
        btc_options = filter_btc_options(products)

        print("Total BTC Options:", len(btc_options))

        if btc_price is None or len(btc_options) == 0:
            print("⚠️ Data not ready")
            time.sleep(10)
            continue

        # ✅ Filter only nearest expiry
        nearest_options = get_nearest_expiry(btc_options)
        print("Nearest Expiry Options:", len(nearest_options))

        # ✅ Select ONE best strike
        best_option = select_best_option(nearest_options, btc_price)

        if best_option:
            print("\n🎯 SELECTED OPTION:")
            print(
                f"{best_option.get('symbol')} | Strike: {best_option.get('strike_price')} | Type: {best_option.get('contract_type')}"
            )
        else:
            print("No option selected")

        time.sleep(15)


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
