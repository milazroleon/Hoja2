# Abstract
from environment_state import EnvironmentState

# Types
from typing import Optional, List, Any

# Libraries
import numpy as np
import matplotlib.pyplot as plt


class ConnectState(EnvironmentState):
    """
    Environment state representation for the Connect Four game.
    """

    def __init__(self, board: Optional[np.ndarray] = None):
        # F = {1,...,6} x {1,...,7} o sea, un tablero 6f x 7c

        if board is None:
            self.board= np.zeros((6,7), dtype=int) 
        else:
            self.board = board

    def is_final(self) -> bool:
        return self.get_winner() != 0 or all(not self.is_col_free(col) for col in range(7))

    def is_applicable(self, event: Any) -> bool:
        
        if isinstance(event,int):
            if 0 <= event < 7 and self.is_col_free(event):
                return True
            else:
                return False

    def transition(self, col: int) -> "EnvironmentState":

        if self.is_applicable(col) is False:
            raise ValueError(f"Not a valid move")

        new_board = self.board.copy()

        row = np.argmax(new_board[::-1, col] == 0)
        actual_row = 5 - row
        count = np.count_nonzero(self.board)
        player = -1 
        
        if count % 2 == 0:
            player = -1
        else:
            player = 1
        new_board[actual_row, col] = player
        return ConnectState(new_board)


    def get_winner(self) -> int:
        
        for row in range(6):
            for col in range(7):
                player = self.board[row, col]
                if player == 0:
                    continue

                # Horizontal
                if col <= 3 and np.all(self.board[row, col:col+4] == player):
                    return player

                # Vertical
                if row <= 2 and np.all(self.board[row:row+4, col] == player):
                    return player

                # Diagonales
                if row <= 2 and col <= 3 and all(self.board[row+i, col+i] == player for i in range(4)):
                    return player

                if row <= 2 and col >= 3 and all(self.board[row+i, col-i] == player for i in range(4)):
                    return player

        return 0

    def is_col_free(self, col: int) -> bool:

        if self.get_heights()[col] < 6:
            return True
        else:
            return False

    def get_heights(self) -> List[int]:

        heights = []

        for col in range(7):
            count=0
            for row in range(6):
                if self.board[row,col] !=0:
                    count += 1
            heights.append(count)

        return heights
    
    def get_free_cols(self) -> List[int]:

        free = []

        for col in range(7):
            if self.is_col_free(col):
                free.append(col)
        return free

    def show(self, size: int = 1500, ax: Optional[plt.Axes] = None) -> None:
        """
        Visualizes the current board state using matplotlib.

        Parameters
        ----------
        size : int, optional
            Size of the stones, by default 1500.
        ax : Optional[matplotlib.axes._axes.Axes], optional
            Axes to plot on. If None, a new figure is created.
        """
        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        pos_red = np.where(self.board == -1)
        pos_yellow = np.where(self.board == 1)

        ax.scatter(pos_yellow[1] + 0.5, 5.5 - pos_yellow[0], color="yellow", s=size)
        ax.scatter(pos_red[1] + 0.5, 5.5 - pos_red[0], color="red", s=size)

        ax.set_ylim([0, self.board.shape[0]])
        ax.set_xlim([0, self.board.shape[1]])
        ax.grid()

        if fig is not None:
            plt.show()

if __name__ == "__main__":
    state = ConnectState()     # Jugada con Rojo como el ganador    
    state = state.transition(0)
    state = state.transition(1)
    state = state.transition(0)
    state = state.transition(1)
    state = state.transition(0)
    state = state.transition(1)
    state = state.transition(0)

    print("Ganador:", state.get_winner())
    state.show()
