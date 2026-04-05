import random

TOTAL_CAPITAL = 1000
TRADES = 100

wins = 0
losses = 0
total_profit = 0


def simulate_trade():
    global wins, losses, total_profit

    # 🔹 Simulated option
    ath = random.uniform(80, 150)
    price = ath

    L1 = ath * 0.1
    L2 = ath * 0.05
    L3 = ath * 0.01

    entries = []
    capital_used = 0

    state = "IDLE"

    for step in range(80):

        # 🔥 realistic mixed movement
        if random.random() < 0.55:
            move = random.uniform(-0.08, -0.01)  # decay
        else:
            move = random.uniform(0.01, 0.12)   # bounce

        price *= (1 + move)

        if price <= 0:
            price = 0.1

        # 🔹 STABILIZATION CHECK
        stable = abs(move) < 0.03

        # =========================
        # ENTRY LOGIC
        # =========================

        if state == "IDLE":

            if price <= L1 and stable:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.2
                state = "ACTIVE"

        elif state == "ACTIVE":

            # ENTRY 2
            if len(entries) == 1 and price <= L2 and stable:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.3

            # ENTRY 3
            elif len(entries) == 2 and price <= L3 and stable:
                if price < entries[-1] * 0.85:
                    entries.append(price)
                    capital_used += TOTAL_CAPITAL * 0.5

        # =========================
        # EXIT LOGIC
        # =========================

        if state == "ACTIVE":

            # 1 entry
            if len(entries) == 1:
                if price >= entries[0] * 1.8:
                    wins += 1
                    total_profit += TOTAL_CAPITAL
                    return

            # multiple entries
            elif len(entries) >= 2:
                if price >= L1:
                    wins += 1
                    total_profit += TOTAL_CAPITAL * 0.3
                    return

    # 🔻 LOSS
    losses += 1
    total_profit -= capital_used


# 🔥 RUN BACKTEST
for _ in range(TRADES):
    simulate_trade()


# 🔥 RESULTS
winrate = (wins / TRADES) * 100

print("\n===== FINAL RESULTS =====")
print("Trades:", TRADES)
print("Wins:", wins)
print("Losses:", losses)
print("Win Rate:", round(winrate, 2), "%")
print("Total Profit:", round(total_profit, 2))
