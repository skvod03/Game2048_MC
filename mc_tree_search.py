from game import Game_2048
import numpy as np

def MC_tree_search(num_steps, N_sim, ax):
    """
    Runs the Monte Carlo Tree Search algorithm to simulate and decide moves for the 2048 game.

    Args:
        num_steps (int): The number of steps to simulate in each random game.
        N_sim (int): The number of simulations to run for each available move.
        ax (matplotlib.axes.Axes): The axes to draw the game state on during each move.
    """
    new_game = Game_2048()
    while True:
        new_game.add_random_number()
        new_game.available_moves()
        new_game.draw_board(ax)

        if len(new_game.available) == 0:
            break

        scores = {}
        for aval_move in new_game.available:
            sim_scores = np.zeros(N_sim)
            for i in range(N_sim):
                attempt_game = Game_2048(np.copy(new_game.state))
                attempt_game.moves[aval_move]()  # Make the move
                attempt_game.random_game(num_steps)  # Perform the random game simulations
                sim_scores[i] = attempt_game.merge_score
            score = np.mean(sim_scores)
            if score not in scores:
                scores[score] = []  # Initialize the list for the given score
            scores[score].append(aval_move)

        best_score = max(scores.keys())  
        best_move = scores[best_score][0]  # Take the first move from the highest score list
        new_game.moves[best_move]()  # Perform the move on the board
        new_game.draw_board(ax)

    print("Game Over!")
    plt.show()
