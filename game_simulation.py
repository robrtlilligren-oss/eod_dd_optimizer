import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ------------------------------
# Function to Run Simulation
# ------------------------------
def run_simulation(
    bet_amount,
    win_rate,
    win_multiplier,
    starting_balance,
    winning_balance,
    initial_drawdown,
    max_trades=1000
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

    if balance <= drawdown_limit:
        return balance, num_bets, "FAIL"

    return balance, num_bets, "INCONCLUSIVE"

# ------------------------------
# Streamlit Interface
# ------------------------------
st.title("EOD DD Planning Tool")

# Input Controls
bet_size = st.slider("Risk Size Dollars", 1, 5000, 239)
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100
win_multiplier = st.slider("RR", 1.00, 5.00, 2.00, 0.1)
starting_balance = st.number_input("Starting Balance", min_value=1000, value=50000)
winning_balance = st.number_input("Passing Balance", min_value=1000, value=53000)
initial_drawdown = st.slider("Maximum Drawdown (Loss Limit)", 500, 10000, 2000)

# Run Simulation
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
            max_trades=1000  # ✅ Explicitly set trade limit
        )
        results.append((score, num_bets, outcome))

    # Extract metrics
    final_scores = [r[0] for r in results]
    num_bets_list = [r[1] for r in results]
    outcomes = [r[2] for r in results]

    wins = outcomes.count("PASS")
    losses = outcomes.count("FAIL")
    inconclusive = outcomes.count("INCONCLUSIVE")

    win_probability = wins / simulations
    loss_probability = losses / simulations
    average_bets = np.mean(num_bets_list)

    # Display Results
    st.subheader("Simulation Results")
    st.write(f"✅ Chance of Hitting Profit Objective: {win_probability:.1%}")
    st.write(f"❌ Chance of Hitting Max DD: {loss_probability:.1%}")
    st.write(f"⚠️ Inconclusive (Did not reach pass/fail in 1000 trades): {inconclusive / simulations:.1%}")
    st.write(f"🔁 Number of Trades Until Pass/Fail: {average_bets:.2f}")

    # Plot Results (Only show true pass/fail balances)
    filtered_scores = [
        r[0] for r in results
        if r[0] >= winning_balance or r[0] <= (starting_balance - initial_drawdown)
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_scores, label='Final Balances', marker='o', linestyle='', markersize=2, color='green')
    ax.axhline(y=winning_balance, color='red', linestyle='--', label="Winning Balance")
    ax.axhline(y=starting_balance - initial_drawdown, color='blue', linestyle='--', label="Drawdown Limit")

    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Final Balance')
    ax.set_title('Simulation Results')
    ax.legend()
    st.pyplot(fig)
