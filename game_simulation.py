import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Function to run simulation
def run_simulation(bet_amount, win_rate, win_multiplier, starting_balance, winning_balance, initial_drawdown, simulations=10000):
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
st.title("End of Day Draw Down Sim")  # Updated title

# Input fields
bet_size = st.slider("Position Size Dollars", 1, 5000, 239)  # Changed to 1 to 5000, label updated
win_rate = st.slider("Win Rate (%)", 0, 100, 50) / 100  # Convert to fraction
win_multiplier = st.slider("RR", 1.00, 5.00, 2.00, 0.1)  # Slider with 2 decimal points for win multiplier
starting_balance = st.number_input("Starting Balance", min_value=1000, value=50000)
winning_balance = st.number_input("Passing Balance", min_value=1000, value=54000)
initial_drawdown = st.slider("Maximum Drawdown (Loss Limit)", 500, 10000, 2000)  # Slider for drawdown limit

# Run simulation button
if st.button("Run Simulation"):
    simulations = 10000
    results = []

    # Run simulation for the selected bet size
    for _ in range(simulations):
        score, num_bets = run_simulation(bet_size, win_rate, win_multiplier, starting_balance, winning_balance, initial_drawdown)
        results.append((score, num_bets))

    # Calculate statistics
    final_scores = [result[0] for result in results]
    num_bets_list = [result[1] for result in results]
    
    wins = sum(1 for score in final_scores if score >= winning_balance)
    losses = sum(1 for score in final_scores if score <= starting_balance - initial_drawdown)
    win_probability = wins / simulations
    loss_probability = losses / simulations
    average_bets = np.mean(num_bets_list)

    # Display results
    st.subheader("Simulation Results")
    st.write(f"Probability of Passing Eval or Not Blowing Account:  {win_probability:.4f}")
    st.write(f"Probability of Failure or Blowing Account:  {loss_probability:.4f}")
    st.write(f"*Difference is simulations that did not terminate in either pass/fail after 1000 trades.")
    st.write(f"Average Number of Trades Until Pass/Fail:  {average_bets:.2f}")  # Changed label here
    


    # Plotting results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(final_scores, label='Final Scores', marker='o', color='green')
    ax.axhline(y=winning_balance, color='red', linestyle='--', label="Winning Balance")
    ax.axhline(y=starting_balance - initial_drawdown, color='blue', linestyle='--', label="Drawdown Limit")
    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Final Balance')
    ax.set_title('Simulation Results')
    ax.legend()
    st.pyplot(fig)
