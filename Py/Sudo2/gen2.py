import numpy as np


def fill_grid(grid, count=0, detect_multiple=False):
    """
    check all possible combinations of numbers until a solution is found and detect  multiple solutions
    """
    for row, col in np.vstack(np.nonzero(grid == 0)).T:
        row_sq, col_sq = row // 3, col // 3
        square = grid[row_sq * 3:row_sq * 3 + 3, col_sq * 3:col_sq * 3 + 3]
        number_list = np.arange(1, 10)
        np.random.shuffle(number_list)
        for value in number_list:
            if not (value in grid[row] or value in grid[:, col] or value in square):  # this value has not been used
                grid[row, col] = value
                if detect_multiple:
                    if np.count_nonzero(grid) == 81:  # grid is full
                        count += 1
                        if count == 2:
                            return False  # we have at least two solutions
                        else:
                            break  # ok, we have one solution, let's check if there is no other one
                    else:
                        fill_grid(grid, count, detect_multiple)
                else:
                    if np.count_nonzero(grid) == 81:
                        return True
                    else:
                        fill_grid(grid)
    return np.count_nonzero(grid) == 81


def init_grid():
    """
    initialise the "canonical" 9 by 9 grid
    """
    grid = np.zeros((9, 9), dtype=int)
    grid[0] = np.arange(1, 10)
    grid[1, 3] = grid[2, 6] = grid[3, 1] = grid[4, 4] = grid[5, 7] = grid[6, 2] = grid[7, 5] = grid[8, 8] = 1
    return grid


def get_nonzero_cell(grid_to_test):
    """
    Select a random cell that is not already empty and not already tested
    """
    rows, cols = grid_to_test.nonzero()
    rows_cols = np.vstack((rows, cols)).T
    np.random.shuffle(rows_cols)
    return rows_cols[0, 0], rows_cols[0, 1]


def print_grid(grid=np.zeros((9, 9))):
    print("+" + "---+" * 9)
    for i, row in enumerate(grid):
        print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+" * 9)
        else:
            print("+" + "   +" * 9)


def generate_partial_grids(grid=np.zeros((9, 9), dtype=int), non_zeros_tg=0):
    """
    generate partial grids with an initial pattern that ensures that the grid is canonical
    """
    if fill_grid(grid):  # Generate a Fully Solved Grid
        grid_to_test = np.copy(grid)

        while 0 < np.count_nonzero(grid_to_test) and np.count_nonzero(grid) - np.count_nonzero(grid_to_test) < non_zeros_tg:
            row, col = get_nonzero_cell(grid_to_test)
            grid_to_test[row, col] = 0  # ok, this cell will have been tested
            backup = grid[row, col]  # Remember its cell value in case we need to put it back
            grid[row, col] = 0
            copy_grid = np.copy(grid)
            if not fill_grid(copy_grid, count=0, detect_multiple=True):
                grid[row, col] = backup
        return grid
    else:
        return False


def put_zeros_on_grid(grid, number_of_zeros=10):
    new_grid = np.copy(grid)
    zeros = min(np.count_nonzero(new_grid), number_of_zeros)
    for _ in range(zeros):
        row, col = get_nonzero_cell(new_grid)
        new_grid[row, col] = 0
    return new_grid


def get_non_zeros_grids(master):
    master_nz = np.copy(master)
    master_nz = master_nz.reshape(82*10, 9, 9)
    master_nz = master_nz[np.count_nonzero(master_nz, axis=(1, 2)) > 0]
    return master_nz


def get_a_good_grid(master):
    r = np.random.random_sample()


def generate_multiple_grids(max_grid=10):
    master_grids = np.load("sudo_master.npy")
    count_per_zeros = np.zeros((82,), dtype=int)
    non_zeros_tg = 40
    step = 0
    while step < 100000:
        non_zero_master = master_grids.reshape((820, 9, 9))
        non_zero_master = [m for m in non_zero_master if 0 < np.count_nonzero(m)]
        max_index = 1 + len(non_zero_master) // 4
        index = np.random.randint(np.random.randint(max_index)+1)
        start_grid = np.copy(non_zero_master[index])
        start_grid = put_zeros_on_grid(start_grid, max(np.count_nonzero(start_grid), np.random.randint(3, 12)))
        init_g = init_grid()
        start_grid = (init_g == 0) * start_grid + init_g
        grid = generate_partial_grids(start_grid, non_zeros_tg)
        if grid:
            non_zeros = np.count_nonzero(grid)
            master_grids[non_zeros, count_per_zeros[non_zeros]] = np.copy(grid)
            count_per_zeros[non_zeros] = min(max_grid-1, count_per_zeros[non_zeros] + 1)
            if 0 < len(np.nonzero(count_per_zeros == max_grid-1)[0]):
                non_zeros_tg = np.nonzero(count_per_zeros == max_grid-1)[0][0]
            step += 1
            if non_zeros < 40:
                print(step, non_zeros_tg, non_zeros)
            if step % 100 == 0:
                np.save(f'sudo_master', master_grids)
                print(step, non_zeros_tg, non_zeros, len(non_zero_master))
    return master_grids


# generate_profound_partial_grids(30)
master = generate_multiple_grids(max_grid=10)



