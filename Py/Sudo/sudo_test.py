import unittest
import numpy as np

from sudo import *


class SudoTestsCase(unittest.TestCase):

    """
    def test_init(self):
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

        slm_calc = sudo.sl_must[1, 0, 1]
        slm = np.array([False, False, True, False, False, False, False, False, True])
        equal_1 = np.array_equal(slm_calc, slm)

        slc_calc = sudo.sc_must[2, 0, 0]
        slc = np.array([False, False, False, False, False, True, False, False, False])
        equal_2 = np.array_equal(slc_calc, slc)

        self.assertEqual(equal_1*equal_2, True)


    def test_sl_must_from_lines(self):
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

        sudo.sl_must_from_must_lines(1, 2, 0)
        slm = np.array([False, True, True, False, False, False, False, True, False])
        slm_calc = sudo.sl_must[1, 2, 0]
        equal_1 = np.array_equal(slm_calc, slm)
        equal_2 = np.array_equal(sudo.sudo[3, 6:9], np.array([2, 8, 3]))

        self.assertEqual(equal_1*equal_2, True)


    def test_sl_must_from_lines(self):
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

        sudo.sl_must_not_from_must_lines(1, 0, 0)
        slm = np.array([True, True, False, False, False, False, False, True, False])
        slm_calc = sudo.sl_must_not[1, 0, 0]
        equal_1 = np.array_equal(slm_calc, slm)
        self.assertEqual(equal_1, True)

    def test_resolution(self):
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

        sudo.line_infer(1, 2)

        sudo.line_infer(1, 1)
        sudo.column_infer(1, 1)

        sudo.column_infer(0, 1)
        self.assertEqual(sudo.sudo[1, 5], 3)
        sudo.line_infer(1, 1)
        sudo.column_infer(1, 1)

        sudo.line_infer(2, 0)

        sudo.column_infer(0, 2)

        sudo.column_infer(1, 2)

        sudo.column_infer(0, 2)
        sudo.line_infer(0, 2)

        sudo.column_infer(2, 2)
        sudo.line_infer(2, 2)

        sudo.column_infer(0, 1)
        sudo.line_infer(0, 1)

        sudo.line_infer(0, 2)
        self.assertEqual(sudo.sudo[0, 8], 2)

        sudo.column_infer(2, 1)
        sudo.line_infer(2, 1)
        self.assertEqual(sudo.sudo[6, 3], 8)

        sudo.line_infer(2, 0)
        sudo.line_infer(2, 1)
        self.assertEqual(sudo.sudo[8, 4], 7)

        sudo.line_infer(2, 2)
        self.assertEqual(sudo.sudo[8, 8], 5)

        sudo.column_infer(0, 2)
        self.assertEqual(sudo.sudo[2, 7], 5)

        sudo.column_infer(2, 1)
        sudo.line_infer(2, 1)
        self.assertEqual(sudo.sudo[7, 4], 5)

        sudo.column_infer(1, 1)
        self.assertEqual(sudo.sudo[4, 3], 6)

        sudo.column_infer(0, 1)

        sudo.line_infer(0, 1)

        sudo.line_infer(0, 0)
        sudo.column_infer(0, 0)

        sudo.column_infer(1, 2)

        sudo.column_infer(2, 2)

        sudo.line_infer(2, 0)
        sudo.column_infer(2, 0)

        sudo.line_infer(0, 0)
        sudo.column_infer(0, 0)

        sudo.line_infer(1, 0)
        sudo.column_infer(1, 0)

        sudo.column_infer(2, 0)

        sudo.line_infer(1, 1)

        sudo.column_infer(0,0)

    def test_number_permutation(self):
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
        sudo.one_in_the_corner()
        sudo.permute_numbers()
        self.assertEqual(sudo.grid[0, 0], 1)
        self.assertEqual(sudo.sudo[0, 0], 1)
        sudo.un_permute_numbers()
        self.assertEqual(sudo.grid[0, 0], 4)
        self.assertEqual(sudo.sudo[0, 0], 4)


        def test_column_permutation(self):
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
    
            sudo.permute_column_for_one(0, 1, 2)
            #self.assertEqual(np.array_equal(sudo.sudo, sudo_start), True)
    
            sudo.un_permute_column()
    
            #self.assertEqual(np.array_equal(sudo.sudo, sudo_start), True)
            #self.assertEqual(np.array_equal(sudo.grid, grid_start), True)
    """

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
