import requests
import time

DELTA_URL = "https://api.delta.exchange"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

previous_price = None


# 🔹 BTC price (reliable)
def get_btc_price():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        data = r.json()
        price = float(data["price"])

        if price < 10000:
            return None

        return price

    except Exception as e:
        print("BTC price error:", e)
        return None


# 🔹 Get products
def get_products():
    try:
        r = requests.get(DELTA_URL + "/v2/products", timeout=5)
        data = r.json()
        return data.get("result", [])
    except Exception as e:
        print("Product error:", e)
        return []


# 🔹 Filter BTC options
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


# 🔹 Nearest expiry
def get_nearest_expiry(options):
    try:
        options = sorted(options, key=lambda x: x.get("settlement_time", ""))
        nearest = options[0].get("settlement_time")

        return [o for o in options if o.get("settlement_time") == nearest]
    except:
        return []


# 🔹 OTM + Direction selection (CORE FIX)
def select_otm_option(options, btc_price, prev_price):
    if prev_price is None:
        return None

    # Decide direction
    direction = "call_options" if btc_price > prev_price else "put_options"

    otm_options = []

    for opt in options:
        try:
            strike = float(opt.get("strike_price", 0))

            if direction == "call_options" and strike > btc_price:
                otm_options.append(opt)

            elif direction == "put_options" and strike < btc_price:
                otm_options.append(opt)

        except:
            continue

    # Pick closest OTM
    best = None
    min_diff = float("inf")

    for opt in otm_options:
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
    global previous_price

    while True:
        print("\n========================")

        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        products = get_products()
        btc_options = filter_btc_options(products)

        print("Total BTC Options:", len(btc_options))

        if not btc_price or not btc_options:
            print("Waiting for data...")
            time.sleep(10)
            continue

        nearest = get_nearest_expiry(btc_options)
        print("Nearest Expiry Options:", len(nearest))

        selected = select_otm_option(nearest, btc_price, previous_price)

        if selected:
            print("\n🎯 SELECTED OTM OPTION:")
            print("Symbol:", selected.get("symbol"))
            print("Strike:", selected.get("strike_price"))
            print("Type:", selected.get("contract_type"))
            print("Expiry:", selected.get("settlement_time"))
        else:
            print("No option selected yet (waiting for direction)")

        # update price memory
        previous_price = btc_price

        time.sleep(15)


if __name__ == "__main__":
    print("🚀 BOT STARTED")
    run()
    
