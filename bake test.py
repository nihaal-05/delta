 import random

TOTAL_CAPITAL = 1000
TRADES = 100

wins = 0
losses = 0
total_profit = 0


def simulate_trade(trade_id):
    global wins, losses, total_profit

    # 🔹 Start option at ATH
    ath = random.uniform(80, 150)
    price = ath

    # 🔹 Levels
    l90 = ath * 0.1
    l95 = ath * 0.05
    l99 = ath * 0.01

    entries = []
    capital_used = 0

    print(f"\n--- Trade {trade_id} ---")
    print("ATH:", round(ath, 2))

    # 🔹 Phase 1: DECAY
    for step in range(20):
        price *= random.uniform(0.75, 0.95)

        # ENTRY 1
        if len(entries) == 0 and price <= l90:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.5
            print("ENTRY 1:", round(price, 2))

        # ENTRY 2
        elif len(entries) == 1 and price <= l95:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.3
            print("ENTRY 2:", round(price, 2))

        # ENTRY 3 (smart)
        elif len(entries) == 2 and price <= l99:
            if price < entries[-1] * 0.8:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.2
                print("ENTRY 3:", round(price, 2))

    # 🔹 Phase 2: RECOVERY / BOUNCE
    for step in range(20):
        price *= random.uniform(1.05, 1.3)

        # EXIT CONDITIONS
        if len(entries) == 1:
            if price >= entries[0] * 2:
                wins += 1
                total_profit += TOTAL_CAPITAL
                print("EXIT 2X:", round(price, 2))
                return

        elif len(entries) >= 2:
            if price >= entries[0]:
                wins += 1
                total_profit += TOTAL_CAPITAL * 0.3
                print("EXIT BREAKEVEN:", round(price, 2))
                return

    # 🔹 LOSS CASE
    losses += 1
    total_profit -= capital_used
    print("LOSS | Capital used:", round(capital_used, 2))


# 🔥 RUN BACKTEST
print("🚀 STARTING BACKTEST...\n")

for i in range(1, TRADES + 1):
    simulate_trade(i)

# 🔥 FINAL RESULTS
print("\n===== FINAL RESULTS =====")
print("Total Trades:", TRADES)
print("Wins:", wins)
print("Losses:", losses)

winrate = (wins / TRADES) * 100
print("Win Rate:", round(winrate, 2), "%")

print("Total Profit:", round(total_profit, 2))
print("Avg Profit per Trade:", round(total_profit / TRADES, 2))
