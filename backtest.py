import random

TOTAL_CAPITAL = 1000
TRADES = 100

wins = 0
losses = 0
total_profit = 0


def simulate_trade():
    global wins, losses, total_profit

    ath = random.uniform(80, 150)
    price = ath

    L1 = ath * 0.1
    L2 = ath * 0.05
    L3 = ath * 0.01

    entries = []
    capital_used = 0

    trade_started = False  # 🔥 important fix

    for step in range(100):

        # realistic movement (balanced)
        if random.random() < 0.55:
            move = random.uniform(-0.08, -0.01)  # decay
        else:
            move = random.uniform(0.01, 0.10)   # bounce

        price *= (1 + move)

        if price <= 0:
            price = 0.1

        # stabilization (kept but fixed)
        stable = abs(move) < 0.06

        # ================= ENTRY =================

        # L1
        if len(entries) == 0 and price <= L1 and stable:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.2
            trade_started = True

        # L2
        elif len(entries) == 1 and price <= L2 and stable:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.3

        # L3
        elif len(entries) == 2 and price <= L3 and stable:
            if price < entries[-1] * 0.85:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.5

        # ================= EXIT =================

        if trade_started:

            # 1 entry → 2x
            if len(entries) == 1:
                if price >= entries[0] * 2:
                    wins += 1
                    total_profit += TOTAL_CAPITAL
                    return

            # multiple entries → exit at L1 LEVEL
            elif len(entries) >= 2:
                if price >= L1:
                    wins += 1
                    total_profit += TOTAL_CAPITAL * 0.3
                    return

    # ================= LOSS =================

    if trade_started:
        losses += 1
        total_profit -= capital_used
    # if no trade started → ignore (correct behavior)


# RUN
for _ in range(TRADES):
    simulate_trade()

# RESULTS
total_trades = wins + losses
winrate = (wins / total_trades) * 100 if total_trades > 0 else 0

print("\n===== FINAL RESULTS =====")
print("Trades Taken:", total_trades)
print("Wins:", wins)
print("Losses:", losses)
print("Win Rate:", round(winrate, 2), "%")
print("Total Profit:", round(total_profit, 2))
