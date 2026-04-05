import requests
import time

DELTA_URL = "https://api.delta.exchange"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

previous_price = None


# 🔹 Get BTC price safely
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


# 🔹 Get products safely
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


# 🔹 Get nearest expiry only
def get_nearest_expiry(options):
    try:
        options = sorted(options, key=lambda x: x.get("settlement_time", ""))
        nearest = options[0].get("settlement_time")

        return [o for o in options if o.get("settlement_time") == nearest]
    except:
        return []


# 🔹 SMART SELECTION (final logic)
def select_smart_option(options, btc_price, prev_price):
    if prev_price is None:
        return None

    momentum = btc_price - prev_price
    threshold = 50  # noise filter

    # 🔥 contrarian decision
    if momentum > threshold:
        side = "put_options"   # market up → choose PE
    elif momentum < -threshold:
        side = "call_options"  # market down → choose CE
    else:
        side = "put_options"   # sideways default

    otm_options = []

    for opt in options:
        try:
            strike = float(opt.get("strike_price", 0))
            opt_type = opt.get("contract_type")

            if opt_type != side:
                continue

            if side == "call_options" and strike > btc_price:
                otm_options.append(opt)

            elif side == "put_options" and strike < btc_price:
                otm_options.append(opt)

        except:
            continue

    # pick closest OTM
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

        print("BTC Options:", len(btc_options))

        if not btc_price or not btc_options:
            print("Waiting for valid data...")
            time.sleep(10)
            continue

        nearest = get_nearest_expiry(btc_options)
        print("Nearest Expiry:", len(nearest))

        selected = select_smart_option(nearest, btc_price, previous_price)

        if selected:
            print("\n🎯 SELECTED OPTION:")
            print("Symbol:", selected.get("symbol"))
            print("Strike:", selected.get("strike_price"))
            print("Type:", selected.get("contract_type"))
            print("Expiry:", selected.get("settlement_time"))
        else:
            print("Waiting for momentum...")

        previous_price = btc_price

        time.sleep(15)  # safe delay


if __name__ == "__main__":
    print("🚀 BOT STARTED (SAFE MODE)")
    run()
