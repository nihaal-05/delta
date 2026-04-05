import requests
import time

DELTA_URL = "https://api.delta.exchange"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

previous_price = None
TOTAL_CAPITAL = 1000  # change if needed


# 🔹 Strategy memory
trade_data = {
    "symbol": None,
    "ath": 0,
    "entries": [],
    "qty": [],
    "position": 0
}


# 🔹 BTC price
def get_btc_price():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        return float(r.json()["price"])
    except:
        return None


# 🔹 Products
def get_products():
    try:
        r = requests.get(DELTA_URL + "/v2/products", timeout=5)
        return r.json().get("result", [])
    except:
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


# 🔹 Smart selection
def select_smart_option(options, btc_price, prev_price):
    if prev_price is None:
        return None

    momentum = btc_price - prev_price
    threshold = 50

    if momentum > threshold:
        side = "put_options"
    elif momentum < -threshold:
        side = "call_options"
    else:
        side = "put_options"

    otm = []

    for opt in options:
        try:
            strike = float(opt.get("strike_price", 0))
            if opt.get("contract_type") != side:
                continue

            if side == "call_options" and strike > btc_price:
                otm.append(opt)
            elif side == "put_options" and strike < btc_price:
                otm.append(opt)
        except:
            continue

    best = None
    min_diff = float("inf")

    for opt in otm:
        try:
            strike = float(opt.get("strike_price", 0))
            diff = abs(strike - btc_price)
            if diff < min_diff:
                min_diff = diff
                best = opt
        except:
            continue

    return best


# 🔹 Option price
def get_option_price(symbol):
    try:
        r = requests.get(DELTA_URL + "/v2/tickers", timeout=5)
        data = r.json()

        for item in data.get("result", []):
            if item.get("symbol") == symbol:
                return float(item.get("mark_price", 0))
        return None
    except:
        return None


# 🔥 STRATEGY ENGINE (FINAL)
def run_strategy(selected):
    global trade_data

    symbol = selected.get("symbol")

    # reset if new option
    if trade_data["symbol"] != symbol:
        trade_data = {
            "symbol": symbol,
            "ath": 0,
            "entries": [],
            "qty": [],
            "position": 0
        }

    price = get_option_price(symbol)
    if not price or price == 0:
        return

    print("Option Price:", price)

    # update ATH
    if price > trade_data["ath"]:
        trade_data["ath"] = price

    ath = trade_data["ath"]
    if ath == 0:
        return

    # levels
    l90 = ath * 0.1
    l95 = ath * 0.05
    l99 = ath * 0.01

    # position sizing
    cap1 = TOTAL_CAPITAL * 0.5
    cap2 = TOTAL_CAPITAL * 0.3
    cap3 = TOTAL_CAPITAL * 0.2

    # ENTRY 1
    if trade_data["position"] == 0 and price <= l90:
        qty = cap1 / price
        trade_data["entries"].append(price)
        trade_data["qty"].append(qty)
        trade_data["position"] += 1
        print("✅ ENTRY 1")

    # ENTRY 2
    elif trade_data["position"] == 1 and price <= l95:
        qty = cap2 / price
        trade_data["entries"].append(price)
        trade_data["qty"].append(qty)
        trade_data["position"] += 1
        print("✅ ENTRY 2")

    # 🔥 SMART ENTRY 3
    elif trade_data["position"] == 2 and price <= l99:
        # extra safety: only if still moving fast
        if price < trade_data["entries"][-1] * 0.8:
            qty = cap3 / price
            trade_data["entries"].append(price)
            trade_data["qty"].append(qty)
            trade_data["position"] += 1
            print("🔥 ENTRY 3 (SMART SMALL SIZE)")

    # EXIT LOGIC
    if trade_data["position"] == 1:
        entry = trade_data["entries"][0]
        if price >= entry * 2:
            print("🎯 EXIT 2X")
            trade_data = {"symbol": None, "ath": 0, "entries": [], "qty": [], "position": 0}

    elif trade_data["position"] >= 2:
        entry = trade_data["entries"][0]
        if price >= entry:
            print("🎯 EXIT BREAKEVEN")
            trade_data = {"symbol": None, "ath": 0, "entries": [], "qty": [], "position": 0}


# 🔹 MAIN LOOP
def run():
    global previous_price

    while True:
        print("\n================")

        btc_price = get_btc_price()
        print("BTC:", btc_price)

        products = get_products()
        btc_options = filter_btc_options(products)

        if not btc_price or not btc_options:
            time.sleep(10)
            continue

        nearest = get_nearest_expiry(btc_options)
        selected = select_smart_option(nearest, btc_price, previous_price)

        if selected:
            print("Selected:", selected.get("symbol"))
            run_strategy(selected)

        previous_price = btc_price
        time.sleep(15)


if __name__ == "__main__":
    print("🚀 BOT STARTED")
    run()
