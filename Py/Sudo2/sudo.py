import numpy as np
import itertools as it


class Sudoku:
    def __init__(self, sudo_init):

        self.sudo_non_canonic = np.copy(sudo_init)
        self.grid = np.copy(sudo_init)
        self.sudo = np.copy(sudo_init)

        #  Sub Line Must (block line x3, block column x3, subline x3, number x9), the number MUST BE in the subline
        self.sl_must = np.zeros((3, 3, 3, 9), dtype=bool)
        #  Sub Line Must Not(block line x3, block column x3, subline x3, number x9), the number CANNOT BE in the subline
        self.sl_must_not = np.zeros((3, 3, 3, 9), dtype=bool)
        # idem for subcolumns
        self.sc_must = np.zeros((3, 3, 3, 9), dtype=bool)
        # idem for subcolumns
        self.sc_must_not = np.zeros((3, 3, 3, 9), dtype=bool)
        # (block line x3, block column x3, number x9, subline x3, subcolumn x3), the number COULD BE in the cell
        self.number = np.ones((3, 3, 9, 3, 3), dtype=bool)

        self.number_permutation = np.arange(10, dtype=int)
        self.column_permutation = np.arange(9, dtype=int)
        self.line_permutation = np.arange(9, dtype=int)

        self.reset()

        # self.solve_grid(0, 0)
        # self.to_canonic()

    def reset(self):
        """
        infer obvious knowledge from the starting grid (and erase previous knowledge if any)
        """
        for ll in range(3):
            for cc in range(3):
                self.bl_must_from_sudo(ll, cc)
                self.bc_must_from_sudo(ll, cc)
                self.number_from_sudo(ll, cc)
                self.sc_must_not = np.zeros((3, 3, 3, 9), dtype=bool)
                self.sl_must_not = np.zeros((3, 3, 3, 9), dtype=bool)

    def bl_must_from_sudo(self, ll: int, cc: int):
        """

        """
        for l_ in range(3):
            self.sl_must_from_sudo(ll, cc, l_)

    def bc_must_from_sudo(self, ll: int, cc: int):
        for c_ in range(3):
            self.sc_must_from_sudo(ll, cc, c_)

    def sl_must_from_sudo(self, ll: int, cc: int, l_: int):
        sl_must = np.in1d(np.arange(9) + 1, self.sudo[3 * ll + l_, 3 * cc:3 * cc + 3])
        self.sl_must[ll, cc, l_] = sl_must

    def sc_must_from_sudo(self, ll: int, cc: int, c_: int):
        sc_must = np.in1d(np.arange(9) + 1, self.sudo[3 * ll: 3 * ll + 3, 3 * cc + c_])
        self.sc_must[ll, cc, c_] = sc_must

    def number_from_sudo(self, ll: int, cc: int):
        block = self.sudo[3 * cc:3 * cc + 3, 3 * ll:3 * ll + 3]
        for num in range(9):
            if np.isin(num + 1, block):
                self.number[cc, ll, num] = (block == num + 1)
            else:
                self.number[cc, ll, num] = (block == 0)

    # external line operations

    def sl_must_from_must_not_lines(self, ll: int, cc: int, l_: int):
        self.sl_must[ll, cc, l_, :] += self.sl_must_not[ll, (cc + 1) % 3, l_] * self.sl_must_not[ll, (cc + 2) % 3, l_]

    def sl_must_not_from_must_lines(self, ll: int, cc: int, l_: int):
        self.sl_must_not[ll, cc, l_] += self.sl_must[ll, (cc+1) % 3, l_] + self.sl_must[ll, (cc+2) % 3, l_]

    # external column operations

    def sc_must_from_must_not_columns(self, ll: int, cc: int, c_: int):
        self.sc_must[ll, cc, c_] += self.sc_must_not[(ll + 1) % 3, cc, c_] * self.sc_must_not[(ll + 2) % 3, cc, c_]

    def sc_must_not_from_must_columns(self, ll: int, cc: int, c_: int):
        self.sc_must_not[ll, cc, c_] += self.sc_must[(ll + 1) % 3, cc, c_] + self.sc_must[(ll + 2) % 3, cc, c_]

    # block line operations

    def sl_must_from_block(self, ll: int, cc: int, l_: int):
        self.sl_must[ll, cc, l_] += self.sl_must_not[ll, cc, (l_ + 1) % 3] * self.sl_must_not[ll, cc, (l_ + 2) % 3]

    def sl_must_not_from_block(self, ll: int, cc: int, l_: int):
        self.sl_must_not[ll, cc, l_] += self.sl_must[ll, cc, (l_ + 1) % 3] + self.sl_must[ll, cc, (l_ + 2) % 3]

    def sl_must_not_from_reverse(self, ll: int, cc: int, l_: int):
        if np.count_nonzero(self.sl_must[ll, cc, l_]) == 3:
            self.sl_must_not[ll, cc, l_] = ~self.sl_must[ll, cc, l_]

    def sl_must_from_reverse(self, ll: int, cc: int, l_: int):
        if np.count_nonzero(self.sl_must_not[ll, cc, l_]) == 6:
            self.sl_must[ll, cc, l_] = ~self.sl_must_not[ll, cc, l_]

    # block column operations

    def sc_must_not_from_block(self, ll: int, cc: int, c_: int):
        self.sc_must_not[ll, cc, c_] += self.sc_must[ll, cc, (c_ + 1) % 3] + self.sc_must[ll, cc, (c_ + 2) % 3]

    def sc_must_from_block(self, ll: int, cc: int, c_: int):
        self.sc_must[ll, cc, c_] += self.sc_must_not[ll, cc, (c_ + 1) % 3] * self.sc_must_not[ll, cc, (c_ + 2) % 3]

    def sc_must_not_from_reverse(self, ll: int, cc: int, c_: int):
        if np.count_nonzero(self.sc_must[ll, cc, c_]) == 3:
            self.sc_must_not[ll, cc, c_] = ~self.sc_must[ll, cc, c_]

    def sc_must_from_reverse(self, ll: int, cc: int, c_: int):
        if np.count_nonzero(self.sc_must_not[ll, cc, c_]) == 6:
            self.sc_must[ll, cc, c_] = ~self.sc_must_not[ll, cc, c_]

    # block from line and column to numbers

    def numbers_from_must_not_line(self, ll, cc, l_):
        for num in np.nonzero(self.sl_must_not[ll, cc, l_])[0]:
            self.number[ll, cc, num, l_, :] = False

    def numbers_from_must_not_column(self, ll, cc, c_):
        for num in np.nonzero(self.sc_must_not[ll, cc, c_])[0]:
            self.number[ll, cc, num, :, c_] = False

    # solve block

    def block_solve(self, ll: int, cc: int, numbers_out=np.zeros(9, dtype=bool), numbers_found=np.zeros(9, dtype=bool)):
        """
        solves numbers within a block: it identifies
        ll : index of the line of the block
        cc : idem for column of the block
        numbers_out :
        numbers_found : list of 9 booleans indicating the numbers found during the current loop

        !!!! numbers go from 1 to 9 but range goes from 0 to 8. The numbers manipulated = num-1

        """
        block = self.sudo[3*ll:3*ll+3, 3*cc:3*cc+3]
        unknowns = np.setdiff1d(np.arange(9)+1, block[block != 0]) - 1  # numbers still unfound (e.g. [3, 4])
        numbers_o = np.arange(9)[numbers_out]
        unknowns = np.setdiff1d(unknowns, numbers_o)

        # there no unknown left
        if len(unknowns) == 0:
            return numbers_found

        # the degree of freedom gives for each number the numbers of cells where it could be
        dof_per_number = np.zeros(len(unknowns), dtype=int)
        for i in range(len(unknowns)):
            dof_per_number[i] = np.count_nonzero(self.number[ll, cc, unknowns[i]])

        # numbers have been found : they have a unique cell where they fit
        singleton_founds = unknowns[dof_per_number == 1]
        if len(singleton_founds) > 0:
            for num in singleton_founds:
                nonz_l, nonz_c = np.nonzero(self.number[ll, cc, num])
                if len(nonz_c) == 0:
                    pass
                else:
                    l_, c_ = nonz_l[0], nonz_c[0]
                self.sudo[3*ll+l_, 3*cc+c_] = num+1
                self.number[ll, cc, ~np.isin(np.arange(9), num)] *= ~self.number[ll, cc, num]
                numbers_found += np.arange(9) == num
                numbers_out += np.arange(9) == num
            self.block_solve(ll, cc, numbers_out=numbers_out, numbers_found=numbers_found)
            return numbers_found

        # duets: two numbers for two cells. They exclude other numbers on the cell
        duets_founds = unknowns[dof_per_number == 2]
        if len(duets_founds) > 1:
            for duet in list(it.combinations(duets_founds, 2)):
                num1, num2 = duet
                product = self.number[ll, cc, num1] * self.number[ll, cc, num2]
                if np.count_nonzero(product) == 2:  # it is a real duet
                    self.number[ll, cc, np.isin(np.arange(9), (num1, num2))] = product
                    self.number[ll, cc, ~np.isin(np.arange(9), (num1, num2))] *= ~product
                    numbers_out += np.isin(np.arange(9), (num1, num2))
                    self.block_solve(ll, cc, numbers_out=numbers_out, numbers_found=numbers_found)
                    return numbers_found

        # triplets : three numbers for three cells
        triplets_founds = unknowns[dof_per_number <= 3]
        if len(triplets_founds) > 2:
            for triplet in list(it.combinations(triplets_founds, 3)):
                num1, num2, num3 = triplet
                product = self.number[ll, cc, num1] * self.number[ll, cc, num2] * self.number[ll, cc, num3]
                if np.count_nonzero(product) == 3:  # it is a real triplet
                    self.number[ll, cc, np.isin(np.arange(9), (num1, num2, num3))] = product
                    self.number[ll, cc, ~np.isin(np.arange(9), (num1, num2, num3))] *= ~product
                    numbers_out += np.isin(np.arange(9), (num1, num2, num3))
                    self.block_solve(ll, cc, numbers_out=numbers_out, numbers_found=numbers_found)
                    return numbers_found

        return numbers_found

        # do we need a quartet?

    # from block to lines and columns

    def sl_must_not_from_numbers(self, ll, cc, l_):
        for num in range(9):
            num_in_sl_must_not = ~np.sum(self.number[ll, cc, num, l_, :], dtype=bool)
            self.sl_must_not[ll, cc, l_, num] = num_in_sl_must_not

    def sc_must_not_from_numbers(self, ll, cc, c_):
        for num in range(9):
            num_in_sc_must_not = ~np.sum(self.number[ll, cc, num, :, c_], dtype=bool)
            self.sc_must_not[ll, cc, c_, num] = num_in_sc_must_not

    # meta operations

    def block_consolidate(self, ll, cc):
        for l_ in range(3):
            self.numbers_from_must_not_line(ll, cc, l_)
        for c_ in range(3):
            self.numbers_from_must_not_column(ll, cc, c_)

        numbers_found = self.block_solve(ll, cc, numbers_out=np.zeros(9, dtype=bool),
                                         numbers_found=np.zeros(9, dtype=bool))

        for l_ in range(3):
            self.sl_must_not_from_numbers(ll, cc, l_)
        for l_ in range(3):
            self.sl_must_from_block(ll, cc, l_)
        for c_ in range(3):
            self.sc_must_not_from_numbers(ll, cc, c_)
        for c_ in range(3):
            self.sc_must_from_block(ll, cc, c_)

        return numbers_found

    def line_infer(self, ll, cc):
        for l_ in range(3):
            self.sl_must_not_from_must_lines(ll, cc, l_)
            self.sl_must_from_must_not_lines(ll, cc, l_)
        for l_ in range(3):
            self.sl_must_from_block(ll, cc, l_)
        numbers_found = self.block_consolidate(ll, cc)
        return numbers_found

    def column_infer(self, ll, cc):
        for c_ in range(3):
            self.sc_must_not_from_must_columns(ll, cc, c_)
            self.sc_must_from_must_not_columns(ll, cc, c_)

        for c_ in range(3):
            self.sc_must_from_block(ll, cc, c_)
        numbers_found = self.block_consolidate(ll, cc)
        return numbers_found

    def infer_from(self, ll, cc, line):
        numbers_found = self.line_infer(ll, cc) if line else self.column_infer(ll, cc)
        return numbers_found

    # utils

    def get_value(self, ll, cc, l_, c_):
        return self.sudo[3*ll+l_, 3*cc+c_]

    def get_block(self, ll, cc, sudo=True):
        return np.copy(self.sudo[3*ll:3*ll+3, 3*cc:3*cc+3]) if sudo else np.copy(self.grid[3*ll:3*ll+3, 3*cc:3*cc+3])

    def print(self, grid=np.zeros((9, 9))):
        if np.count_nonzero(grid) == 0:
            grid = self.sudo_non_canonic
        print("+" + "---+" * 9)
        for i, row in enumerate(grid):
            print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
            if i % 3 == 2:
                print("+" + "---+" * 9)
            else:
                print("+" + "   +" * 9)

    # permutations

    def permute_numbers(self):
        first_line = np.copy(self.grid[0])
        self.number_permutation[1:10] = first_line
        self.sudo += 10
        self.grid += 10
        self.sudo[self.sudo == 10] = 0
        for num in range(1, 10):
            self.sudo[self.sudo == self.number_permutation[num]+10] = num
            self.grid[self.grid == self.number_permutation[num]+10] = num

    def un_permute_numbers(self):
        self.sudo_non_canonic += 10
        self.sudo_non_canonic[self.sudo_non_canonic == 10] = 0
        self.grid += 10
        self.grid[self.grid == 10] = 0
        for num in range(1, 10):
            permu_num = self.number_permutation[num]
            self.sudo[self.sudo_non_canonic == num+10] = permu_num
            self.grid[self.grid == num+10] = permu_num

    def permute_column_for_one(self, ll, cc, c_):
        block = self.get_block(ll, cc, sudo=False)
        _, col_one = np.nonzero(block == 1)
        col_one = col_one[0]
        co_one = 3*cc+col_one
        co = 3*cc+c_
        self.sudo[:, [co, co_one]] = self.sudo[:, [co_one, co]]
        self.grid[:, [co, co_one]] = self.grid[:, [co_one, co]]
        original_co = self.column_permutation[co]
        original_co_one = self.column_permutation[co] = co_one
        self.column_permutation[co] = original_co_one
        self.column_permutation[co_one] = original_co

    def permute_line_for_one(self, ll, cc, l_):
        block = self.get_block(ll, cc, sudo=False)
        line_one, _ = np.nonzero(block == 1)
        line_one = line_one[0]
        li_one = 3*ll+line_one
        li = 3*ll+l_
        self.sudo[[li, li_one], :] = self.sudo[[li_one, li], :]
        self.grid[[li, li_one], :] = self.grid[[li_one, li], :]
        original_li = self.line_permutation[li]
        original_li_one = self.line_permutation[li_one]
        self.line_permutation[li] = original_li_one
        self.line_permutation[li_one] = original_li

    def un_permute_columns(self):
        for co in range(9):
            co_one = self.column_permutation[co]
            self.sudo_non_canonic[:, [co, co_one]] = self.sudo_non_canonic[:, [co_one, co]]
            self.grid[:, [co, co_one]] = self.grid[:, [co_one, co]]
            self.column_permutation[co] = co
            self.column_permutation[co_one] = co_one

    def un_permute_lines(self):
        for li in range(9):
            li_one = self.line_permutation[li]
            self.sudo[[li, li_one], :] = self.sudo[[li_one, li], :]
            self.grid[[li, li_one], :] = self.grid[[li_one, li], :]
            self.line_permutation[li] = li
            self.line_permutation[li_one] = li_one

    def to_canonic(self):
        for ll in range(2):
            for cc in range(3):
                self.permute_column_for_one(ll, cc, c_=ll)
        for ll in range(3):
            for cc in range(2):
                self.permute_line_for_one(ll, cc, l_=cc)
        self.permute_numbers()

    def from_canonic(self):
        self.sudo_non_canonic = np.copy(self.sudo)
        self.un_permute_columns()
        self.un_permute_lines()
        self.un_permute_numbers()

    def check_grid(self, row, col, num):
        for x in range(9):
            if self.grid[row][x] == num:
                return False
        for x in range(9):
            if self.grid[x][col] == num:
                return False
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve_grid(self, row, col):
        M = 9
        if row == M - 1 and col == M:
            return True
        if col == M:
            row += 1
            col = 0
        if self.grid[row][col] > 0:
            return self.solve_grid(row, col + 1)
        for num in range(1, M + 1, 1):
            if self.check_grid(row, col, num):
                self.grid[row][col] = num
                if self.solve_grid(row, col + 1):
                    return True
            self.grid[row][col] = 0
        return False
