# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_core.ipynb.

# %% auto 0
__all__ = ['Game']

# %% ../00_core.ipynb 3
from collections import Counter
from itertools import cycle

import numpy as np
from fastcore.basics import patch

from .exceptions import ColumnFullError

# %% ../00_core.ipynb 6
class Game():
    """
    Class that controls the whole game. It keeps track of both boards.
    """
    def __init__(self,
                 n_players=2, # Number of players.
                 board_size=3, # Size of the board. It is a squared grid of `board_size`x`board_size`
                 ):
        self.n_players = n_players
        self.board_size = board_size
        self.boards = np.zeros(shape=(n_players, board_size, board_size))
        self.current_player = self.choose_initial_player()
        self._players = cycle(range(n_players))

    def __repr__(self):
        """
        Representation of the game state.
        The current player is marked with an *.
        """
        player0 = "Player 1 *" if self.current_player==0 else "Player 1"
        player1= "Player 2 *" if self.current_player==1 else "Player 2"
        
        return "\n".join([player0,
                          str(self.boards[0]),
                          player1,
                          str(self.boards[1])])
        
    def choose_initial_player(self):
        """
        The initial player is chosen at random at the beggining of the game.
        """
        return np.random.choice([0,1])
    
    def _change_player(self):
        """
        Changes the current player.
        """
        # return next(self._players)
        self.current_player = next(self._players)

    def is_done(self):
        """
        The game is considered finished when one of the boards is completed.
        This can be checked by checking if there are any 0s left in a board.
        """
        return (not (self.boards[0] == 0).any()) or (not (self.boards[1] == 0).any())

    def add_dice(self,
                 player, # Player to add the dice to.
                 column, # Column where we want to place the dice.
                 dice, # Dice to place.
                 ):
        """
        Adds a dice to the corresponding player in the specified column.
        """
        board_column = self.boards[player][:,column]
        idxs_dice = np.where(board_column==0)[0]
        if len(idxs_dice)==0: raise ColumnFullError # Can't place dice in a full column.
        board_column[idxs_dice[0]] = dice
        return self.is_done()

# %% ../00_core.ipynb 12
@patch
def score(self: Game,
          player, # Number of the player we want to calculate the score.
          ):
    """
    Returns the calculated score for a player. 
    If there are numbers repeated in a column, 
    their values must be added and multiplied by the number of repetitions. 
    Otherwise, they are added. If there are repreated and non-repeated in the same column, 
    the repeated are summed and multiplied by the number of repetitions and then the result is added to the non-repeated.
    """
    total = 0
    for col in self.boards[player].T: # Transposed to iterate over the columns
        cntr = Counter(col)
        sum_col = sum([n*reps*reps for n, reps in cntr.items()])
        total += sum_col
    return total

# %% ../00_core.ipynb 15
@patch
def __repr__(self: Game):
    """
    Representation of the game state.
    The current player is marked with an *.
    """
    player0 = f"Player 1 ({self.score(0)})"
    player1 = f"Player 2 ({self.score(1)})"
    player0 = f"{player0} *" if self.current_player==0 else player0
    player1= f"{player1} *" if self.current_player==1 else player1
    
    return "\n".join([player0,
                      str(self.boards[0]),
                      player1,
                      str(self.boards[1])])

# %% ../00_core.ipynb 17
@patch
def _pad_player_board(self: Game,
                      player: str, # Player __repr__
                      board: str, # Board __repr__
                      ):
    """
    Pads the representation of a player indicator and a board
    so that each line has the same characters.
    """
    max_len = max(max(map(len, board.split("\n"))), len(player))
    return "\n".join(map(lambda x: x.ljust(max_len, " "), "\n".join([player, board]).split("\n")))

# %% ../00_core.ipynb 18
@patch
def _join_players_boards(self: Game,
                         playerboard1: str, # Padded playerboard obtained from `._pad_player_board()`.
                         playerboard2: str, # Padded playerboard obtained from `._pad_player_board()`.
                         separator: str = " | ", # Character used as a separator.
                         ):
    """
    Join two padded player boards with a separator in between.
    """
    n_lines = max(playerboard1.count("\n"), playerboard2.count("\n")) + 1 # Last line doesn't have \n.
    separator = "\n".join([separator]*n_lines)

    split_lines = zip(playerboard1.split("\n"), separator.split("\n"))
    res = "\n".join([s1 + s2 for s1, s2 in split_lines])
    split_lines = zip(res.split("\n"), playerboard2.split("\n"))
    res = "\n".join([s1 + s2 for s1, s2 in split_lines])
    return res

# %% ../00_core.ipynb 19
@patch
def __repr__(self: Game):
    """
    Representation of the game state.
    The current player is marked with an *.
    """
    player0 = f"Player 1 ({self.score(0)})"
    player1 = f"Player 2 ({self.score(1)})"
    player0 = f"{player0} *" if self.current_player==0 else player0
    player1= f"{player1} *" if self.current_player==1 else player1

    board0 = str(self.boards[0])
    board1 = str(self.boards[1])
    
    padded0 = self._pad_player_board(player0, board0)
    padded1 = self._pad_player_board(player1, board1)
    
    return self._join_players_boards(padded0, padded1)

# %% ../00_core.ipynb 22
@patch
def play_turn(self: Game):
    """
    Plays a full turn.
    """
    dice = np.random.choice(range(1,7))
    print(f"Dice to place: {dice}")
    print(self)
    column = int(input("Select column: "))
    self.add_dice(player=self.current_player,
                  column=column,
                  dice=dice)
    self._change_player()
