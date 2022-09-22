# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_gym.ipynb.

# %% auto 0
__all__ = ['MatatenaEnv']

# %% ../02_gym.ipynb 2
from itertools import cycle

import numpy as np
from fastcore.basics import patch

import gym
from gym import spaces

from .core import *

# %% ../02_gym.ipynb 5
class MatatenaEnv(gym.Env, Game):
    """
    `gym`-ready implementation of `Game`.
    """
    metadata = {"render_modes":["human"],
                "render_fps":4}

    def __init__(self, **kwargs):
        super(MatatenaEnv, self).__init__(**kwargs)
        self.action_space = spaces.Discrete(self.board_size)
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(low=0,  high=6, shape=(3,3), dtype=np.uint8),
                "opponent": spaces.Box(low=0,  high=6, shape=(3,3), dtype=np.uint8),
                "dice": spaces.Discrete(6)
            }
        )

# %% ../02_gym.ipynb 10
@patch
def reset(self: MatatenaEnv,
          seed: int=None, # Seed to control the RNG.
          options=None # Additional options.
          ): # Initial state of the environment.
    """
    Reinitializes the environment and returns the initial state.
    """
    super(MatatenaEnv, self).reset(seed=seed)

    self.boards = np.zeros(shape=(self.n_players, self.board_size, self.board_size))
    self.current_player = self.choose_initial_player()
    self._players = cycle(range(self.n_players))
    opposite_players_mask = np.arange(self.boards.shape[0]) != self.current_player
    self.last_dice = np.random.choice(range(1,7))
    observation =  {
      "agent": self.boards[self.current_player],
      "opponent": self.boards[opposite_players_mask].squeeze(),
      "dice": self.last_dice,
    }
    info = None
    
    return (observation, info)

# %% ../02_gym.ipynb 15
@patch
def step(self: MatatenaEnv,
         action, # Action to be executed on the environment. Should be the column in which the agent wants to place the dice.
         ): # (observation, reward, done, info) tuple.

    ## 1. Add the dice to the desired column
    self.add_dice(player=self.current_player,
                  column=action,
                  dice=self.last_dice)
    
    ## 2. Check if the game is done
    done = self.is_done()

    ## 3. Give rewards regarding if they win or not
    if done:
        scores = [self.score(player) for player in range(self.n_players)]
        reward = 1 if scores[self.current_player] == max(scores) else -1
    else:
        reward = 0

    ## 4. Roll a new dice and change current player
    self.last_dice = np.random.choice(range(1,7))  
    self._change_player()
    
    ## 5. Build new observation
    opposite_players_mask = np.arange(self.boards.shape[0]) != self.current_player
    observation =  {
      "agent": self.boards[self.current_player],
      "opponent": self.boards[opposite_players_mask].squeeze(),
      "dice": self.last_dice,
    }
    
    return observation, reward, done, None

# %% ../02_gym.ipynb 17
@patch
def render(self: MatatenaEnv):
    print(self.__repr__())