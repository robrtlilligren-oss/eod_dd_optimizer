import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def run_simulation(
    bet_amount,
    win_rate,
    win_multiplier,
    starting_balance,
    winning_balance,
    initial_drawdown,
    simulations=10000,
    max_trades=1000,
):
    balance = starting_balance
    drawdown_limit = starting_balance - initial_drawdown
    max_balance = balance
    num_bets = 0

    while balance > drawdown_limit and num_bets < max_trades:
        if np.random.rand() < win_rate:
            balance += bet_amount * win_multiplier
        else:
            balance -= bet_amount

        max_balance = max(max_balance, balance)
        if balance >= max_balance:
            drawdown_limit = max_balance - initial_drawdown

        if balance >= winning_balance:
            return balance, num_bets, "PASS"

        num_bets += 1

    # Final check after loop
    if balance >= winning_balance:
        return balance, num_bets, "PASS"
    elif balance <= drawdown_limit:
        return balance, num_bets, "FAIL"
    else:
        return balance, num_bets, "INCONCLUSIVE"


st.title("EOD DD Planning Tool")

bet_size = st.slider("Risk Size Dollars", 1, 5000, 239)
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100
win_multiplier = st.slider("RR", 1.00, 5.00, 2.00, 0.1)
starting_balance = st.number_input("Starting Balance", min_value=1000, value=50000)
winning_balance = st.number_input("Passing Balance", min_value=1000, value=53000)
initial_drawdown = st.slider("Maximum Drawdown (Loss Limit)", 500, 10000, 2000)

if st.button("Run Simulation"):
    simulations = 10000
    results = []

    for _ in range(simulations):
        score, num_bets, outcome = run_simulation(
            bet_size,
            win_rate,
            win_multiplier,
            starting_balance,
            winning_balance,
            initial_drawdown,
            simulations,
        )
        results.append((score, num_bets, outcome))

    final_scores = [r[0] for r in results]
    num_bets_list = [r[1] for r in results]
    outcomes = [r[2] for r in results]

    wins = outcomes.count("PASS")
    losses = outcomes.count("FAIL")
    inconclusive = outcomes.count("INCONCLUSIVE")

    win_probability = wins / simulations
    loss_probability = losses / simulations
    inconclusive_probability = inconclusive / simulations
    average_bets = np.mean(num_bets_list)

    st.subheader("Simulation Results")
    st.write(f"✅ Chance of Passing Eval/Hitting Profit Objective: {win_probability:.1%}")
    st.write(f"❌ Probability of Failure or Blowing Account: {loss_probability:.1%}")
    st.write(f"⚠️ Inconclusive (Did not reach pass/fail in 1000 trades): {inconclusive_probability:.1%}")
    st.write(f"🔁 Number of Trades Until Pass/Fail or Max Trades: {average_bets:.2f}")

    scores_all = [r[0] for r in results]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        scores_all,
        label="Final Scores (All outcomes)",
        marker="o",
        linestyle="None",
        color="green",
        markersize=3,
    )
    ax.axhline(y=winning_balance, color="red", linestyle="--", label="Winning Balance")
    ax.axhline(
        y=starting_balance - initial_drawdown,
        color="blue",
        linestyle="--",
        label="Drawdown Limit",
    )
    ax.set_xlabel("Simulation Number")
    ax.set_ylabel("Final Balance")
    ax.set_title("Simulation Results")
    ax.legend()
    st.pyplot(fig)
