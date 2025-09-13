import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Simulation Function
# -----------------------------
def run_simulation(bet_amount, win_rate, win_multiplier, starting_balance, winning_balance, initial_drawdown):
    balance = starting_balance
    drawdown_limit = starting_balance - initial_drawdown
    max_balance = balance
    num_bets = 0

    while balance > drawdown_limit:
        if np.random.rand() < win_rate:
            balance += bet_amount * win_multiplier
        else:
            balance -= bet_amount

        max_balance = max(max_balance, balance)
        drawdown_limit = max_balance - initial_drawdown

        if balance >= winning_balance:
            return "win", balance, num_bets

        num_bets += 1

    return "loss", balance, num_bets


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("EOD DD Planning Tool")

# Input fields
bet_size = st.slider("Risk Size Dollars", 1, 5000, 239)
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100.0
win_multiplier = st.slider("RR", 1.00, 5.00, 2.00, 0.1)
starting_balance = st.number_input("Starting Balance", min_value=1000, value=50000)
winning_balance = st.number_input("Passing Balance", min_value=1000, value=53000)
initial_drawdown = st.slider("Maximum Drawdown (Loss Limit)", 500, 10000, 2000)

# Run simulation button
if st.button("Run Simulation"):
    simulations = 10000
    results = []

    for _ in range(simulations):
        outcome, final_balance, num_bets = run_simulation(
            bet_size,
            win_rate,
            win_multiplier,
            starting_balance,
            winning_balance,
            initial_drawdown
        )
        results.append((outcome, final_balance, num_bets))

    final_scores = [r[1] for r in results]
    num_bets_list = [r[2] for r in results]

    wins = sum(1 for r in results if r[0] == "win")
    win_probability = wins / simulations
    average_bets = np.mean(num_bets_list)

    # Display results
    st.subheader("Simulation Results")
    st.write(f"Chance of Passing Eval/Hitting Profit Objective:  {win_probability:.1%}")
    st.write(f"Number of Trades Until Pass/Fail:  {average_bets:.2f}")

    # Plotting results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(final_scores, label='Final Scores', marker='o', color='green', linestyle='None', markersize=2)
    ax.axhline(y=winning_balance, color='red', linestyle='--', label="Winning Balance")
    ax.axhline(y=starting_balance - initial_drawdown, color='blue', linestyle='--', label="Drawdown Limit")
    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Final Balance')
    ax.set_title('Simulation Results')
    ax.legend()
    st.pyplot(fig)
