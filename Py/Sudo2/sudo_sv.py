import numpy as np
import itertools as it


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


class Sudoku:
    def __init__(self, sudo=sudo_grid):
        self.sudo = sudo
        self.sl_must = np.zeros((3, 3, 3, 9), dtype=bool)
        self.sl_must_not = np.zeros((3, 3, 3, 9), dtype=bool)
        self.sc_must = np.zeros((3, 3, 3, 9), dtype=bool)
        self.sc_must_not = np.zeros((3, 3, 3, 9), dtype=bool)
 #       self.cell_must_not = np.zeros((3, 3, 3, 3, 9), dtype=bool)
 #       self.cell = np.zeros((3, 3, 3, 3), dtype=int)
        self.number = np.ones((3, 3, 9, 3, 3), dtype=bool)

        for ll in range(3):
            for cc in range(3):
                self.bl_must_from_sudo(ll, cc)
                self.bc_must_from_sudo(ll, cc)
                self.number_from_sudo(ll, cc)


    # setters
    def set_sudo(self, ll=0, cc=0, l_=0, c_=0, number=0, li=-1, co=-1):
        if li == -1:
            li = ll*3+l_
        if co == -1:
            co = cc*3+c_
        self.sudo[li, co] = number

    def set_must(self, ll: int, cc: int, idx: int, sub: np.ndarray, line: bool, must=True, incremental=True):
        if line:
            l_ = idx
            if must:
                must_line = sub
                if incremental:
                    self.sl_must[ll, cc, l_] += must_line
                else:
                    self.sl_must[ll, cc, l_] = must_line
            else:
                must_not_line = sub
                if incremental:
                    self.sl_must_not[ll, cc, l_] += must_not_line
                else:
                    self.sl_must_not[ll, cc, l_] = must_not_line
        else:
            c_ = idx
            if must:
                must_column = sub
                if incremental:
                    self.sc_must[ll, cc, c_] += must_column
                else:
                    self.sc_must[ll, cc, c_] = must_column

                pass
            else:
                must_not_column = sub
                if incremental:
                    self.sc_must_not[ll, cc, c_] += must_not_column
                else:
                    self.sc_must_not[ll, cc, c_] = must_not_column

    def bl_must_from_sudo(self, ll: int, cc: int):
        for l_ in range(3):
            self.sl_must_from_sudo(ll, cc, l_)

    def bc_must_from_sudo(self, ll: int, cc: int):
        for c_ in range(3):
            self.sc_must_from_sudo(ll, cc, c_)

    def sl_must_from_sudo(self, ll: int, cc: int, l_: int):
        sl_must = np.in1d(np.arange(9) + 1, self.sudo[3 * ll + l_, 3 * cc:3 * cc + 3])
        self.set_must(ll, cc, l_, sl_must, line=True)

    def sc_must_from_sudo(self, ll: int, cc: int, c_: int):
        sc_must = np.in1d(np.arange(9) + 1, self.sudo[3 * ll: 3 * ll + 3, 3 * cc + c_])
        self.set_must(ll, cc, c_, sc_must, line=False)

    def number_from_sudo(self, ll: int, cc: int):
        block = self.sudo[3 * cc:3 * cc + 3, 3 * ll:3 * ll + 3]
        for num in range(9):
            if np.isin(num+1, block):
                self.number[cc, ll, num] = (block == num+1)
            else:
                self.number[cc, ll, num] = (block == 0)


    # external line operations

    """
    def sl_must_not_from_sc_must_not(self, ll: int, cc: int, l_: int):
        subline = self.sudo[3*ll+l_, 3*cc:3*cc+3]
        self.sl_must_not[ll, cc, l_] += np.prod(self.sc_must_not[ll, cc, subline == 0], axis=0, dtype=bool)
    """

    def sl_must_from_must_not_lines(self, ll: int, cc: int, l_: int):
        self.sl_must[ll, cc, l_, :] += self.sl_must_not[ll, (cc + 1) % 3, l_] * self.sl_must_not[ll, (cc + 2) % 3, l_]

    def sl_must_not_from_must_lines(self, ll: int, cc: int, l_: int):
        self.sl_must_not[ll, cc, l_] += self.sl_must[ll, (cc+1) % 3, l_] + self.sl_must[ll, (cc+2) % 3, l_]

    """
    def sl_must_from_must_lines(self, ll: int, cc: int, l_: int):
        must_line = self.sl_must[ll, (cc+1) % 3, l_] + self.sl_must[ll, (cc+2) % 3, l_]
        if np.count_nonzero(must_line) == 6:
            self.sl_must[ll, cc, l_] = ~must_line

    def sl_must_not_from_must_not_lines(self, ll: int, cc: int, l_: int):
        must_not_line = self.sl_must_not[ll, (cc+1) % 3, l_] * self.sl_must_not[ll, (cc+2) % 3, l_]
        if np.count_nonzero(must_not_line) == 6:
            self.sl_must[ll, cc, l_] = ~must_line
    """
    # external column operations
    """
    def sc_must_not_from_sc_must_not(self, ll: int, cc: int, c_: int):
        subcol = self.sudo[3*ll:3*ll+3, 3*cc+c_]
        self.sc_must_not[ll, cc, c_] += np.prod(self.sl_must_not[ll, cc, subcol == 0], axis=0, dtype=bool)
    """

    def sc_must_from_must_not_columns(self, ll: int, cc: int, c_: int):
        self.sc_must[ll, cc, c_] += self.sc_must_not[(ll + 1) % 3, cc, c_] * self.sc_must_not[(ll + 2) % 3, cc, c_]

    def sc_must_not_from_must_columns(self, ll: int, cc: int, c_: int):
        self.sc_must_not[ll, cc, c_] += self.sc_must[(ll + 1) % 3, cc, c_] + self.sc_must[(ll + 2) % 3, cc, c_]

    """"
    def sc_must_from_must_columns(self, ll: int, cc: int, c_: int):
        must_col = self.sc_must[(ll + 1) % 3, cc, c_] + self.sc_must[(ll + 2) % 3, cc, c_]
        if np.count_nonzero(must_col) == 6:
            self.sc_must[ll, cc, c_] = ~must_col
    """
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

    def block_solve(self, ll, cc, numbers_out=np.zeros(9, dtype=bool)):

        block = self.sudo[3*ll:3*ll+3, 3*cc:3*cc+3]
        unknowns = np.setdiff1d(np.arange(9)+1, block[block != 0]) - 1
        numbers_o = np.arange(9)[numbers_out]
        unknowns = np.setdiff1d(unknowns, numbers_o)

        if len(unknowns) == 0:
            return

        dof_per_number = np.zeros(len(unknowns), dtype=int)

        for i in range(len(unknowns)):
            dof_per_number[i] = np.count_nonzero(self.number[ll, cc, unknowns[i]])

        singleton_founds = unknowns[dof_per_number == 1]
        if len(singleton_founds) > 0:
            for num in singleton_founds:
                nonz_l, nonz_c = np.nonzero(self.number[ll, cc, num])
                l_, c_ = nonz_l[0], nonz_c[0]
                self.sudo[3*ll+l_, 3*cc+c_] = num+1
                self.number[ll, cc, ~np.isin(np.arange(9), num), self.number[ll, cc, num]] = False
            self.block_solve(ll, cc, np.zeros(9, dtype=bool))
            return

        duets_founds = unknowns[dof_per_number == 2]
        if len(duets_founds) > 1:
            for duet in list(it.combinations(duets_founds, 2)):
                num1, num2 = duet
                product = self.number[ll, cc, num1] * self.number[ll, cc, num2]
                if np.count_nonzero(product) == 2:  # it is a real duet
                    self.number[ll, cc, np.isin(np.arange(9), (num1, num2))] = product
                    self.number[ll, cc, ~np.isin(np.arange(9), (num1, num2))] *= ~product
                    numbers_out += np.isin(np.arange(9), (num1, num2))
                    self.block_solve(ll, cc, numbers_out)
                    return

        triplets_founds = unknowns[dof_per_number <= 3]
        if len(triplets_founds) > 2:
            for triplet in list(it.combinations(triplets_founds, 3)):
                num1, num2, num3 = triplet
                product = self.number[ll, cc, num1] * self.number[ll, cc, num2] * self.number[ll, cc, num3]
                if np.count_nonzero(product) == 3:  # it is a real triplet
                    self.number[ll, cc, np.isin(np.arange(9), (num1, num2, num3))] = product
                    self.number[ll, cc, ~np.isin(np.arange(9), (num1, num2, num3))] *= ~product
                    numbers_out += np.isin(np.arange(9), (num1, num2, num3))
                    self.block_solve(ll, cc, numbers_out)
                    return

        return

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

        out_numbers = np.zeros(9, dtype=bool)
        self.block_solve(ll, cc, out_numbers)

        for l_ in range(3):
            self.sl_must_not_from_numbers(ll, cc, l_)
        for l_ in range(3):
            self.sl_must_from_block(ll, cc, l_)
        for c_ in range(3):
            self.sc_must_not_from_numbers(ll, cc, c_)
        for c_ in range(3):
            self.sc_must_from_block(ll, cc, c_)

    def line_infer(self, ll, cc):
        for l_ in range(3):
            self.sl_must_not_from_must_lines(ll, cc, l_)
            self.sl_must_from_must_not_lines(ll, cc, l_)
        for l_ in range(3):
            self.sl_must_from_block(ll, cc, l_)
        self.block_consolidate(ll, cc)

    def column_infer(self, ll, cc):
        for c_ in range(3):
            self.sc_must_not_from_must_columns(ll, cc, c_)
            self.sc_must_from_must_not_columns(ll, cc, c_)

        for c_ in range(3):
            self.sc_must_from_block(ll, cc, c_)
        self.block_consolidate(ll, cc)

    def get_value(self, ll, cc, l_, c_):
        return self.sudo[3*ll+l_, 3*cc+c_]

    def print(self):
        print("+" + "---+" * 9)
        for i, row in enumerate(self.sudo):
            print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
            if i % 3 == 2:
                print("+" + "---+" * 9)
            else:
                print("+" + "   +" * 9)


""" do we need those?

    def cell_must_not_from_line(self, ll: int, cc: int, l_: int):
        self.cell_must_not[ll, cc, l_] += self.sl_must_not[ll, cc, l_]

    def cell_must_not_from_column(self, ll: int, cc: int, c_: int):
        self.cell_must_not[ll, cc, c_] += self.sc_must_not[ll, cc, c_]

    # cell to cell

    def cell_must_from_cell_in_line(self, ll: int, cc: int, l_: int, c_: int):
        cell_must = self.sl_must * \
                    (self.cell_must_not[ll, cc, l_, (c_+1) % 3] + self.cell_must_not[ll, cc, l_, (c_+2) % 3])
        if np.count_nonzero(cell_must) == 1:
            self.cell[ll, cc, l_, c_] = (np.arange(9)[cell_must]+1)[0]

    def cell_must_from_cell_in_column(self, ll: int, cc: int, l_: int, c_: int):
        cell_must = self.sc_must * \
                    (self.cell_must_not[ll, cc, (l_+1) % 3, c_] + self.cell_must_not[ll, cc, (l_+2) % 3, c_])
        if np.count_nonzero(cell_must) == 1:
            self.cell[ll, cc, l_, c_] = (np.arange(9)[cell_must]+1)[0]

    # do we need this one?
    def sl_must_from_must_lines(self, ll: int, cc: int, l_: int):
        sl_must_plus_1 = self.sl_must[ll, (cc + 1) % 3, (l_ + 1) % 3] \
                             + self.sl_must[ll, (cc + 2) % 3, (l_ + 1) % 3]
        sl_must_plus_2 = self.sl_must[ll, (cc + 1) % 3, (l_ + 2) % 3] \
                             + self.sl_must[ll, (cc + 2) % 3, (l_ + 2) % 3]
        self.sl_must[ll, cc, l_, :] += sl_must_plus_1 * sl_must_plus_2




    def sudo_from_sl_must(self, ll: int, cc: int, l_: int):
        sl_must = self.sl_must[ll, cc, l_]
        sl_sudo = self.sudo[3*ll+l_, 3*cc:3*cc+3]
        if np.count_nonzero(sl_sudo) == 2 and np.count_nonzero(sl_must) == 3:
            numbers = np.arange(9)[sl_must] + 1
            mask = np.in1d(numbers, sl_sudo, invert=True)
            sl_sudo[sl_sudo == 0] = numbers[mask][0]
            self.sudo[3*ll+l_, 3*cc:3*cc+3] = sl_sudo
            self.bc_must_from_sudo(ll, cc)

    def sudo_from_sl_must_and_sc_must_not(self, ll: int, cc: int, l_: int, c_: int):
        sl_must = self.sl_must[ll, cc, l_]
        sc_must_not = self.sc_must_not[ll, cc, c_]
        sl_sudo = self.sudo[3*ll+l_, 3*cc:3*cc+3]
        if np.count_nonzero(sl_sudo) == 1 and np.count_nonzero(sl_must) == 3:
            numbers = np.arange(9)[sl_must] + 1
            mask = np.in1d(numbers, sl_sudo, invert=True)
            sl_sudo[sl_sudo == 0] = numbers[mask][0]
            self.sudo[3*ll+l_, 3*cc:3*cc+3] = sl_sudo
            self.bc_must_from_sudo(ll, cc)

    def sudo_from_sc_must(self, ll: int, cc: int, c_: int):
        sc_must = self.sc_must[ll, cc, c_]
        sc_sudo = self.sudo[3*ll:3*ll+3, 3*cc+c_]
        if np.count_nonzero(sc_sudo) == 2 and np.count_nonzero(sc_must) == 3:
            numbers = np.arange(9)[sc_must] + 1
            mask = np.in1d(numbers, sc_sudo, invert=True)
            sc_sudo[sc_sudo == 0] = numbers[mask][0]
            self.sudo[3*ll:3*ll+3, 3*cc+c_] = sc_sudo
            self.bl_must_from_sudo(ll, cc)



    # to be divided into 3 operations?
    def sudo_from_sc_and_sl_must(self, ll: int, cc: int, l_: int, c_: int):
        li = 3*ll+l_
        co = 3*cc+c_
        intersection = self.sl_must[ll, cc, l_] * self.sc_must[ll, cc, c_]
        if np.count_nonzero(intersection) == 1:
            self.sudo[li, co] = np.nonzero(intersection)[0][0]+1

    # end of operations

    # metaoperation

    def do_operation(self, cc, ll, line, index, opid):
        if opid == 0:
            return self.sl_must_not_from_must_lines(cc, ll, index) if line \
                else self.sc_must_not_from_must_columns(cc, ll, index)


"""
