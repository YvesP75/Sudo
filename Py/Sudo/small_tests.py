import numpy as np


def plus_one(arr):
    arr += 1
    return arr


arr = np.ones((3, 3))
arr2 = plus_one(arr)
arr3=arr

a = np.ones((3, 3, 3, 3))
b = a.reshape((9, 3, 3))

aa = np.ones((3, 3))
bb = np.zeros((3, 3))
bb[0] = [1, 1, 1]

