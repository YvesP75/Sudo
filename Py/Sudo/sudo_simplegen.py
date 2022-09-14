import numpy as np
from numpy import ndarray


class SimpleGen:
    def __init__(self, grid_index=0):
        grids = np.load("sudo_master.npy")
        grids = grids.reshape((820, 9, 9))
        grids = [m for m in grids if 0 < np.count_nonzero(m)]
        grid_index = max(0, len(grids) - grid_index - 1)
        self.sudo_grid = grids[grid_index]
        self.sudo_grid_sv: ndarray = np.array([
            [4, 0, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 9, 8],
            [3, 0, 0, 0, 8, 2, 4, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 8, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 6, 7, 0],
            [0, 5, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 9, 0, 7],
            [6, 4, 0, 3, 0, 0, 0, 0, 0],
        ])



