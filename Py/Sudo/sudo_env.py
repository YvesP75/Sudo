import gym
from gym import spaces
import numpy as np

from sudo import Sudoku
from sudo_simplegen import SimpleGen

MAX_LOOP = 7
STABILITY = 3


class SudoEnv(gym.Env):

    def __init__(self):

        super(SudoEnv, self).__init__()

        self.grid = SimpleGen().sudo_grid

        self.sudo = Sudoku(self.grid)
        self.cost_multiplier = 0.1
        self.cost = 1
        self.reward = 2
        self.count = 0
        self.step_number = 0
        self.cumulated_reward = 0
        self.last_cumulated_reward = -300
        self.best_reward = -300
        self.stability = 0   # number of iterations with the same total cost (if == 5 then change of grid)
        self.grid_index = 0

        self.observation_space = spaces.MultiBinary(729)  # 81 cells with 9 numbers
        self.action_space = spaces.Discrete(18)  # 9 boxes and 2 possible inferences

    def reset(self):
        if self.stability == STABILITY:
            self.grid_index += 1
            self.grid = SimpleGen(self.grid_index).sudo_grid
            print("new grid")
        self.sudo = Sudoku(self.grid)
        self.cost = 1  # cost per step
        self.step_number = 0
        self.reward = 2  # reward per number found
        self.count = 1  # number of loops before finding a number
        self.cumulated_reward = 0  # cumulated cost on the trajectory

        obs = self.sudo.number.flatten()
        return obs

    def render(self, mode=''):
        pass

    def step(self, action: int):

        block, line = divmod(action, 2)  # line inference if True else column inference for the block(3,3)
        ll, cc = divmod(block, 3)  # ll = the line index of the block and cc the column's

        #  Mr Sudo, can you make an inference from line or column from this block defined by ll and cc?
        numbers_found = self.sudo.infer_from(ll, cc, line)
        numbers_found_in_step = np.count_nonzero(numbers_found)
        success = np.count_nonzero(self.sudo.sudo) == 81

        if 0 < numbers_found_in_step:
            self.cost = 1
            self.count = 0
            self.sudo.reset()
            reward = self.reward * numbers_found_in_step
        else:
            self.count += 1
            self.cost = self.cost * (1 + self.cost_multiplier) if self.count < MAX_LOOP else 100 - self.cumulated_reward
            reward = -self.cost

        self.cumulated_reward += reward

        obs = self.sudo.number.flatten()

        done = success or self.count == MAX_LOOP
        if done:
            self.best_reward = max(self.best_reward, self.cumulated_reward)
            stable = abs(self.cumulated_reward - self.last_cumulated_reward) < max(3., 0.2 * abs(self.cumulated_reward))
            self.stability += 1 if stable and success else 0
            self.last_cumulated_reward = self.cumulated_reward
        info = {'numbers_found': numbers_found}

        return obs, reward, done, info

    def close(self):
        pass
