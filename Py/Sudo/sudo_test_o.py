import unittest
import numpy as np

from sudo import *


class SudoTestsCase(unittest.TestCase):

    def test_init(self):
        sudo_grid = np.array([
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
        sudo = Sudoku(sudo_grid)
        sudo.print()
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
        sudo.print()
        print(sudo.sl_must[1, 2, 0])
        sudo.sl_must_from_must_lines(1, 2, 0)
        slm = np.array([False, True, True, False, False, False, False, True, False])
        slm_calc = sudo.sl_must[1, 2, 0]
        equal_1 = np.array_equal(slm_calc, slm)

        sudo.sudo_from_sl_must(1, 2, 0)
        sudo.print()
        print(sudo.sudo[3, 6:9])
        equal_2 = np.array_equal(sudo.sudo[3, 6:9], np.array([2, 8, 3]))

        self.assertEqual(equal_1*equal_2, True)

    def test_sl_must_not_from_sc_must_not(self):
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
        sudo.print()
        print(sudo.sl_must_not[1, 0, 0])
        sudo.sl_must_not_from_must_lines(1, 0, 0)
        print(sudo.sl_must_not[1, 0, 0])
        slm = np.array([True, True, False, False, False, False, False, True, False])
        slm_calc = sudo.sl_must_not[1, 0, 0]
        equal_1 = np.array_equal(slm_calc, slm)

        self.assertEqual(equal_1, True)

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
        sudo.print()
        print(sudo.sl_must_not[1, 0, 0])
        sudo.sl_must_not_from_must_lines(1, 0, 0)
        print(sudo.sl_must_not[1, 0, 0])
        slm = np.array([True, True, False, False, False, False, False, True, False])
        slm_calc = sudo.sl_must_not[1, 0, 0]
        equal_1 = np.array_equal(slm_calc, slm)
        self.assertEqual(equal_1, True)

    def test_sl_must_not_from_sc_must_not(self):
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

        sudo.sc_must_not_from_must_columns(0, 1, 0)
        sudo.sc_must_not_from_must_columns(0, 1, 1)
        sudo.sl_must_not_from_sc_must_not(0, 1, 0)
        sudo.sl_must_not_from_must_lines(0, 1, 2)
        sudo.sl_must_from_block(0, 1, 1)

        slm = np.array([False, False, True, False, False, False, False, False, False])
        slm_calc = sudo.sl_must_not[0, 1, 0]
        equal_1 = np.array_equal(slm_calc, slm)
        self.assertEqual(equal_1, True)

        sudo.sc_must_from_block(0, 1, 2)
        sudo.sudo_from_sc_and_sl_must(0, 1, 1, 2)
        self.assertEqual(sudo.get_value(0, 1, 1, 2), 3)

        sudo.sc_must_not_from_must_columns(0, 2, 1)
        sudo.sc_must_not_from_must_columns(0, 2, 2)
        sudo.sc_must_from_block(0, 2, 0)
        sudo.sudo_from_sc_must(0, 2, 0)
        self.assertEqual(sudo.get_value(0, 2, 0, 0), 7)

        sudo.sl_must_not_from_must_lines(1, 2, 1)
        sudo.sl_must_not_from_must_lines(1, 2, 2)
        sudo.sl_must_from_block(1, 2, 0)
        sudo.sudo_from_sl_must(1, 2, 0)
        self.assertEqual(sudo.get_value(1, 2, 0, 2), 3)
        sudo.print()

        sudo.sc_must_not_from_must_columns(0, 2, 2)
        sudo.sc_must_not_from_reverse(0, 2, 0)
        sudo.sc_must_from_block(0, 2, 1)

        sudo.sl_must_not_from_must_lines(0, 2, 2)
        sudo.sl_must_not_from_reverse(0, 2, 1)
        sudo.sl_must_from_block(0, 2, 0)

        sudo.sudo_from_sc_and_sl_must(0, 2, 0, 1)

        self.assertEqual(sudo.get_value(0, 2, 0, 1), 3)


        sudo.sc_must_not_from_must_columns(2, 0, 0)
        sudo.sc_must_not_from_must_columns(2, 0, 2)
        sudo.sc_must_from_block(2, 0, 1)
        sudo.sudo_from_sc_must(2, 0, 1)
        self.assertEqual(sudo.get_value(2, 0, 1, 1), 3)


        sudo.sl_must_not_from_must_lines(2, 0, 0)
        sudo.sl_must_not_from_must_lines(2, 0, 1)
        sudo.sl_must_from_block(2, 0, 2)
        sudo.sudo_from_sl_must(2, 0, 2)
        self.assertEqual(sudo.get_value(2, 0, 2, 2), 9)
        sudo.print()

        sudo.sl_must_not_from_reverse(1, 2, 0)
        sudo.sl_must_not_from_must_lines(1, 2, 1)
        sudo.sl_must_from_block(1, 2, 2)
        sudo.sudo_from_sl_must(1, 2, 2)
        self.assertEqual(sudo.get_value(1, 2, 2, 2), 9)
        sudo.print()


        sudo.sl_must_not_from_reverse(1, 2, 0)
        sudo.sl_must_not_from_must_lines(1, 2, 1)
        sudo.sl_must_from_block(1, 2, 2)
        sudo.sudo_from_sl_must(1, 2, 2)
        self.assertEqual(sudo.get_value(1, 2, 2, 2), 9)
        sudo.print()


        sudo.sl_must_not_from_must_lines(1, 1, 1)
        sudo.sl_must_not_from_must_lines(1, 1, 2)
        sudo.sl_must_from_block(1, 1, 2)
        sudo.sc_must_not_from_must_columns(1, 1, 2)
















if __name__ == '__main__':
    unittest.main()
