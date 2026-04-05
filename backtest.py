 import random

TOTAL_CAPITAL = 1000
TRADES = 200

wins = 0
losses = 0
total_profit = 0

win_amounts = []
loss_amounts = []


def simulate_trade():
    global wins, losses, total_profit

    ath = random.uniform(80, 150)
    price = ath

    # levels
    l90 = ath * 0.1
    l95 = ath * 0.05
    l99 = ath * 0.01

    entries = []
    capital_used = 0

    for step in range(60):

        # 🔥 realistic movement (FIXED)
        if random.random() < 0.6:
            move = random.uniform(-0.12, -0.02)  # decay
        else:
            move = random.uniform(0.02, 0.18)   # bounce

        price *= (1 + move)

        if price <= 0:
            price = 0.1

        # ENTRY 1
        if len(entries) == 0 and price <= l90:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.5

        # ENTRY 2
        elif len(entries) == 1 and price <= l95:
            entries.append(price)
            capital_used += TOTAL_CAPITAL * 0.3

        # ENTRY 3 (SMART)
        elif len(entries) == 2 and price <= l99:
            if price < entries[-1] * 0.8:
                entries.append(price)
                capital_used += TOTAL_CAPITAL * 0.2

        # EXIT

        # 1 entry → 1.8x (realistic)
        if len(entries) == 1:
            if price >= entries[0] * 1.8:
                profit = TOTAL_CAPITAL
                total_profit += profit
                win_amounts.append(profit)
                wins += 1
                return

        # 2+ entries → recovery exit
        elif len(entries) >= 2:
            if price >= entries[0]:
                profit = TOTAL_CAPITAL * 0.3
                total_profit += profit
                win_amounts.append(profit)
                wins += 1
                return

    # LOSS
    losses += 1
    total_profit -= capital_used
    loss_amounts.append(capital_used)


# 🔥 RUN BACKTEST
for _ in range(TRADES):
    simulate_trade()


# 🔥 METRICS
winrate = (wins / TRADES) * 100

avg_win = sum(win_amounts) / len(win_amounts) if win_amounts else 0
avg_loss = sum(loss_amounts) / len(loss_amounts) if loss_amounts else 1

rr = avg_win / avg_loss if avg_loss != 0 else 0


# 🔥 FINAL OUTPUT
print("\n===== FINAL BACKTEST RESULTS =====")
print("Trades:", TRADES)
print("Wins:", wins)
print("Losses:", losses)
print("Win Rate:", round(winrate, 2), "%")
print("Total Profit:", round(total_profit, 2))
print("RR Ratio:", round(rr, 2))
