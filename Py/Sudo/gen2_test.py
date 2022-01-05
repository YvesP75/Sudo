import unittest
import numpy as np

from sudo import *


class Gen2TestCase(unittest.TestCase):


    def test_to_canonic(self):
        sudo_grid = np.array([
            [4, 0, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 9, 8],
            [3, 0, 0, 0, 8, 2, 4, 0, 0],
            [0, 0, 0, 1, 0, 0, 2, 8, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 6, 7, 0],
            [0, 5, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 9, 0, 7],
            [6, 4, 0, 3, 0, 0, 0, 0, 0],
        ])

        sudo = Sudoku(sudo_grid)
        sudo_start = np.copy(sudo.sudo)
        grid_start = np.copy(sudo.grid)

        print("BEFORE")
        sudo.print(grid_start)

        print("TO")
        sudo.to_canonic()
        sudo.print(sudo.grid)

        sudo.from_canonic()
        print("FROM")
        sudo.print(sudo.grid)

        self.assertEqual(np.array_equal(sudo.grid, grid_start), True)












if __name__ == '__main__':
    unittest.main()
