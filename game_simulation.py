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
    simulations=10000
):
    balance = starting_balance
    drawdown_limit = starting_balance - initial_drawdown
    max_balance = balance
    num_bets = 0

    while balance > drawdown_limit:
        # Simulate a single trade
        if np.random.rand() < win_rate:
            balance += bet_amount * win_multiplier
        else:
            balance -= bet_amount

        max_balance = max(max_balance, balance)

        # Adjust drawdown limit based on max balance
        if balance >= max_balance:
            drawdown_limit = max_balance - initial_drawdown

        # Exit condition if profit target is hit
        if balance >= winning_balance:
            return balance, num_bets

        num_bets += 1

    return balance, num_bets

# ------------------------------
# Streamlit Interface
# ------------------------------
st.title("EOD DD Planning Tool")

# Input Controls
bet_size = st.slider("Risk Size ($)", 1, 5000, 239)
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100  # Converted to decimal
win_multiplier = st.slider("Reward-to-Risk (RR)", 1.0, 5.0, 2.0, 0.1)
starting_balance = st.number_input("Starting Balance ($)", min_value=1000, value=50000)
winning_balance = st.number_input("Profit Target ($)", min_value=1000, value=53000)
initial_drawdown = st.slider("Max Drawdown ($)", 500, 10000, 2000)

# Run Simulation
if st.button("Run Simulation"):
    simulations = 10000
    results = []

    for _ in range(simulations):
        score, num_bets = run_simulation(
            bet_size, win_rate, win_multiplier,
            starting_balance, winning_balance,
            initial_drawdown
        )
        results.append((score, num_bets))

    # Extract final scores and trade counts
    final_scores = [r[0] for r in results]
    num_bets_list = [r[1] for r in results]

    # Calculate metrics
    wins = sum(1 for score in final_scores if score >= winning_balance)
    losses = sum(1 for score in final_scores if score <= starting_balance - initial_drawdown)
    win_probability = wins / simulations
    loss_probability = losses / simulations
    average_bets = np.mean(num_bets_list)

    # ------------------------------
    # Display Results
    # ------------------------------
    st.subheader("Simulation Results")
    st.write(f"Chance of Hitting Profit Target: **{win_probability:.1%}**")
    # st.write(f"Probability of Blowing Account: **{loss_probability:.1%}**")
    # st.write("*Note: Some simulations may not end in pass/fail after 1,000 trades.")
    st.write(f"🔁 Average Number of Trades Until Pass/Fail: **{average_bets:.2f}**")

    # ------------------------------
    # Plot Results
    # ------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(final_scores, label='Final Balances', marker='o', linestyle='', markersize=2, color='green')
    ax.axhline(y=winning_balance, color='red', linestyle='--', label="Profit Target")
    ax.axhline(y=starting_balance - initial_drawdown, color='blue', linestyle='--', label="Drawdown Limit")

    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Final Balance ($)')
    ax.set_title('Simulation Outcomes')
    ax.legend()
    st.pyplot(fig)
