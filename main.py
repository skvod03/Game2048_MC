import matplotlib.pyplot as plt
from mc_tree_search import MC_tree_search

def main():
    """
    Main function that initializes the game and runs the Monte Carlo Tree Search.

    The game starts, and the Monte Carlo Tree Search is performed to simulate moves.
    The final state is drawn on the matplotlib axes.
    """
    num_steps = 4  # Number of steps to simulate in each random game
    N_sim = 100  # Number of simulations per move

    # Create the plot and axes once
    fig, ax = plt.subplots(figsize=(4, 4))

    # Run MC Tree Search
    MC_tree_search(num_steps, N_sim, ax)

if __name__ == "__main__":
    main()
