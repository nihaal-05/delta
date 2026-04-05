import requests
import time

DELTA_URL = "https://api.delta.exchange"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


# 🔹 Get BTC price (RELIABLE)
def get_btc_price():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        data = r.json()
        price = float(data["price"])

        if price < 10000:
            raise Exception("Invalid BTC price")

        return price

    except Exception as e:
        print("❌ BTC price error:", e)
        return None


# 🔹 Get products
def get_products():
    try:
        r = requests.get(DELTA_URL + "/v2/products", timeout=5)
        data = r.json()
        return data.get("result", [])
    except Exception as e:
        print("❌ Product fetch error:", e)
        return []


# 🔹 Filter BTC options ONLY
def filter_btc_options(products):
    result = []

    for p in products:
        try:
            if (
                "option" in str(p.get("contract_type", "")).lower()
                and p.get("underlying_asset", {}).get("symbol") == "BTC"
                and p.get("state") == "live"
            ):
                result.append(p)
        except:
            continue

    return result


# 🔹 Get nearest expiry
def get_nearest_expiry(options):
    try:
        options = sorted(options, key=lambda x: x.get("settlement_time", ""))
        nearest = options[0].get("settlement_time")

        filtered = [o for o in options if o.get("settlement_time") == nearest]

        return filtered
    except:
        return []


# 🔹 Select best ATM strike (ONLY ONE)
def select_atm_option(options, btc_price):
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
def run():
    while True:
        print("\n==============================")

        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        products = get_products()
        print("Total Products:", len(products))

        btc_options = filter_btc_options(products)
        print("BTC Options:", len(btc_options))

        if not btc_price or not btc_options:
            print("⚠️ Waiting for valid data...")
            time.sleep(10)
            continue

        nearest = get_nearest_expiry(btc_options)
        print("Nearest Expiry Options:", len(nearest))

        if not nearest:
            print("⚠️ No nearest expiry options")
            time.sleep(10)
            continue

        best = select_atm_option(nearest, btc_price)

        if best:
            print("\n🎯 FINAL SELECTED OPTION:")
            print("Symbol:", best.get("symbol"))
            print("Strike:", best.get("strike_price"))
            print("Type:", best.get("contract_type"))
            print("Expiry:", best.get("settlement_time"))
        else:
            print("⚠️ No option selected")

        time.sleep(15)


if __name__ == "__main__":
    print("🚀 BOT STARTED")
    run()
