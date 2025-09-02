import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Function to run simulation
def run_simulation(bet_amount, win_rate, win_multiplier, starting_balance, winning_balance, initial_drawdown=2000, simulations=10000):
    balance = starting_balance
    drawdown_limit = starting_balance - initial_drawdown
    max_balance = balance
    num_bets = 0
    while balance > drawdown_limit:
        if np.random.rand() < win_rate:
            balance += bet_amount * win_multiplier
        else:
            balance += bet_amount * -1
        max_balance = max(max_balance, balance)
        if balance >= max_balance:
            drawdown_limit = max_balance - initial_drawdown
        if balance >= winning_balance:
            return balance, num_bets
        num_bets += 1
    return balance, num_bets

# Streamlit interface
st.title("Game Simulation Settings")

# Input fields
bet_size = st.slider("Bet Size", 100, 1000, 500)
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100  # Convert to fraction
win_multiplier = st.slider("Win Multiplier", 1, 5, 2)
starting_balance = st.number_input("Starting Balance", min_value=1000, value=50000)
winning_balance = st.number_input("Winning Balance", min_value=1000, value=54000)

# Run simulation button
if st.button("Run Simulation"):
    simulations = 10000
    results = []

    # Run simulation for the selected bet size
    for _ in range(simulations):
        score, num_bets = run_simulation(bet_size, win_rate, win_multiplier, starting_balance, winning_balance)
        results.append((score, num_bets))

    # Calculate statistics
    final_scores = [result[0] for result in results]
    num_bets_list = [result[1] for result in results]
    
    wins = sum(1 for score in final_scores if score >= winning_balance)
    losses = sum(1 for score in final_scores if score <= starting_balance - 2000)
    win_probability = wins / simulations
    loss_probability = losses / simulations
    average_bets = np.mean(num_bets_list)

    # Display results
    st.subheader("Simulation Results")
    st.write(f"Win Probability: {win_probability:.4f}")
    st.write(f"Loss Probability: {loss_probability:.4f}")
    st.write(f"Average Bets: {average_bets:.2f}")

    # Plotting results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(final_scores, label='Final Scores', marker='o', color='green')
    ax.axhline(y=winning_balance, color='red', linestyle='--', label="Winning Balance")
    ax.axhline(y=starting_balance - 2000, color='blue', linestyle='--', label="Drawdown Limit")
    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Final Balance')
    ax.set_title('Simulation Results')
    ax.legend()
    st.pyplot(fig)
