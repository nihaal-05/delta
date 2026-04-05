import random

TOTAL_CAPITAL = 1000

wins = 0
losses = 0
total_profit = 0
trades = 50  # keep small first


def simulate_trade():
    global wins, losses, total_profit

    ath = random.uniform(50, 150)

    l90 = ath * 0.1
    l95 = ath * 0.05
    l99 = ath * 0.01

    price = ath

    entries = []
    capital_used = 0

    for step in range(30):

        price *= random.uniform(0.7, 0.98)

        # ENTRY 1
        if len(entries) == 0 and price <= l90:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.5
            print("Entry 1 at", price)

        # ENTRY 2
        elif len(entries) == 1 and price <= l95:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.3
            print("Entry 2 at", price)

        # ENTRY 3
        elif len(entries) == 2 and price <= l99:
            if price < entries[-1] * 0.8:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.2
                print("Entry 3 at", price)

        # EXIT
        if len(entries) == 1 and price >= entries[0] * 2:
            wins += 1
            total_profit += TOTAL_CAPITAL
            print("Exit 2x")
            return

        elif len(entries) >= 2 and price >= entries[0]:
            wins += 1
            total_profit += TOTAL_CAPITAL * 0.3
            print("Exit BE")
            return

    losses += 1
    total_profit -= capital_used
    print("Loss")


# 🔥 RUN
print("Starting backtest...\n")

for i in range(trades):
    print(f"\n--- Trade {i+1} ---")
    simulate_trade()

print("\n===== FINAL RESULTS =====")
print("Trades:", trades)
print("Wins:", wins)
print("Losses:", losses)
print("Win Rate:", (wins / trades) * 100)
print("Total Profit:", total_profit)
