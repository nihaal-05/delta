import requests
import time

BASE_URL = "https://api.delta.exchange"

# Get BTC price
def get_btc_price():
    try:
        url = BASE_URL + "/v2/tickers"
        response = requests.get(url)
        data = response.json()

        for item in data["result"]:
            if item.get("symbol") == "BTCUSD":
                return float(item.get("last_price"))

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


# Filter BTC options
 def filter_btc_options(products):
    btc_options = []

    for p in products:
        try:
            # Correct fields for Delta
            if (
                p.get("contract_type") == "call_option"
                or p.get("contract_type") == "put_option"
            ):
                if p.get("underlying") == "BTC":
                    btc_options.append(p)

        except:
            continue

    return btc_options

        # BTC price
        btc_price = get_btc_price()
        print("BTC Price:", btc_price)

        # Products
        products = get_all_products()
        print("Total products:", len(products))

        # Filter BTC options
        btc_options = filter_btc_options(products)
        print("BTC Options Found:", len(btc_options))

        # Print sample options
        print("\nSample Options:")
        for opt in btc_options[:5]:
            print(
                f"{opt.get('symbol')} | Strike: {opt.get('strike_price')} | Expiry: {opt.get('expiry_date')}"
            )

        time.sleep(15)


if __name__ == "__main__":
    print("Bot started...")
    run_bot()
