import numpy as np

a = np.array([0, 1, 2, 3, 4, 5])
b = np.array([[6, 7], [8, 9], [10, 11]])
size = 2
pointer = 0

for i in range(len(b)):
    a[pointer: pointer + size] = b[i][:]
    pointer += size

print(a)
