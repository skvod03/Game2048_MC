import numpy as np
import matplotlib.pyplot as plt

class Game_2048():
    """
    Class representing the 2048 game board and its mechanics.

    Attributes:
        state (numpy.ndarray): The 4x4 grid representing the game state.
        merge_score (int): The score accumulated from merged tiles.
        moves (dict): Dictionary mapping moves ('l', 'r', 'u', 'd') to methods.
        available (list): List of available moves at any given moment.
    """

    def __init__(self, start_state=None):
        """
        Initializes the game state, setting up the grid and score.

        Args:
            start_state (numpy.ndarray, optional): Initial game state. Defaults to None.
        """
        if start_state is None:
            self.state = np.zeros((4, 4), dtype=int)
        else:
            self.state = start_state.astype(int)
        self.merge_score = 0
        self.moves = {'l': self.left_move, 'r': self.right_move, 'u': self.up_move, 'd': self.down_move}
        self.available = []

    def shift_left(self, arr):
        """
        Shifts all non-zero elements to the left in a given array.

        Args:
            arr (numpy.ndarray): The array to shift.

        Returns:
            numpy.ndarray: The array with non-zero elements shifted left.
        """
        non_zero = arr[np.where(arr != 0)]
        res = np.zeros_like(arr)
        res[:len(non_zero)] = non_zero
        return res

    def merge(self, arr):
        """
        Merges the array by combining adjacent equal numbers and calculating score.

        Args:
            arr (numpy.ndarray): The array to merge.

        Returns:
            tuple: The merged array and the score obtained from merging.
        """
        score = 0
        for i in range(len(arr) - 1):
            if arr[i] == arr[i+1]:
                arr[i] *= 2
                score += arr[i]
                arr[i+1] = 0
        return arr, score

    def shift_merge(self, arr):
        """
        Shifts and merges the array.

        Args:
            arr (numpy.ndarray): The array to shift and merge.

        Returns:
            tuple: The merged and shifted array and the score obtained.
        """
        shifted = self.shift_left(arr)
        merged_arr, score = self.merge(shifted)
        return self.shift_left(merged_arr), score

    def left_move(self):
        """
        Perform a move to the left, shifting and merging tiles in the game state.
        Updates the merge_score attribute with the score obtained from merging.
        """
        tot_score = 0
        for i in range(len(self.state[0])):
            row = self.state[i]
            self.state[i], score = self.shift_merge(row)
            tot_score += score
        self.merge_score += tot_score

    def right_move(self):
        """
        Perform a move to the right, by first flipping the board horizontally,
        calling the left_move method, and flipping it back.
        """
        self.state = np.flip(self.state, axis=1)
        self.left_move()
        self.state = np.flip(self.state, axis=1)

    def up_move(self):
        """
        Perform a move upwards, by first transposing the board, calling the left_move method, 
        and transposing it back.
        """
        self.state = self.state.T
        self.left_move()
        self.state = self.state.T

    def down_move(self):
        """
        Perform a move downwards, by first transposing the board, calling the right_move method, 
        and transposing it back.
        """
        self.state = self.state.T
        self.right_move()
        self.state = self.state.T

    def add_random_number(self):
        """
        Adds a random number (either 2 or 4) to a randomly chosen empty spot on the board.
        """
        number = np.random.choice([2, 4], p=[0.9, 0.1])
        available_coords = np.where(self.state == 0)
        idx = np.random.choice(len(available_coords[0])) 
        self.state[available_coords[0][idx], available_coords[1][idx]] = number

    def available_moves(self):
        """
        Checks which moves are available by comparing the current state to a simulated state
        after each potential move. Updates the available moves list.
        """
        available = []
        cur_merge_sum = self.merge_score
        for move in self.moves.keys():
            board_copy = self.state.copy()
            self.moves[move]()
            if np.any(board_copy != self.state):
                available.append(move)
            self.state = board_copy
        self.available = available
        self.merge_score = cur_merge_sum

    def random_game(self, num_steps):
        """
        Runs a random game simulation by adding random numbers and making random moves.

        Args:
            num_steps (int): The number of steps to simulate.
        """
        for _ in range(num_steps):
            self.add_random_number()
            self.available_moves()
            if len(self.available) == 0:
                break
            move = np.random.choice(self.available)
            self.moves[move]()

    def draw_board(self, ax):
        """
        Draws the current state of the board on the provided matplotlib axes.

        Args:
            ax (matplotlib.axes.Axes): The axes to draw the board on.
        """
        ax.clear()  # Clear the current axes to update the plot
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        ax.set_title(f"Score: {self.merge_score}", fontsize=12)

        tile_colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#3c3a32"
        }

        for i in range(4):
            for j in range(4):
                val = self.state[i, j]
                color = tile_colors.get(val, "#3c3a32")
                ax.add_patch(plt.Rectangle((j, 3 - i), 1, 1, facecolor=color, edgecolor='black'))

                if val != 0:
                    text_color = "#776e65" if val <= 4 else "white"
                    ax.text(j + 0.5, 3 - i + 0.5, str(val), ha='center', va='center',
                            fontsize=16, weight='bold', color=text_color)

        plt.draw()
        plt.pause(0.1)
