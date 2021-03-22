import numpy as np
from random import uniform
import time

MIN, MAX = 0, 20
a0, a1, a2, a3 = 1, 2, 2, 3

X = np.empty((8, 3), dtype=float)
Y = np.empty(8)
X0 = np.empty(3)
DX = np.empty(3)
XNormal = np.empty((8, 3), dtype=float)

start_time = time.time()
for i in range(8):
    for j in range(3):
        X[i, j] = uniform(MIN, MAX)

for i in range(8):
    Y[i] = a0 + a1 * X[i, 0] + a2 * X[i, 1] + a3 * X[i, 2]

for i in range(3):
    X0[i] = (X[:, i].max() + X[:, i].min()) / 2
    DX[i] = X[:, i].max() - X0[i]

Y_et = a0 + a1 * X0[0] + a2 * X0[1] + a3 * X0[2]

for i in range(8):
    for j in range(3):
        XNormal[i, j] = (X[i, j] - X0[j]) / DX[j]

dY = 9999
number = -1

for i in range(8):
    if Y[i] - Y_et < dY and Y[i] - Y_et > 0:
        dY = Y[i] - Y_et
        number = i

Y2 = a0 + a1 * X[number, 0] + a2 * X[number, 1] + a3 * X[number, 2]

stop_time = time.time()

print("X:\n", X)
print("Y:\n", Y)
print("X0: \n", X0)
print("T_et = ", Y_et)
print("XNormalized: \n", XNormal.round(4))
print("number = ", number)
print("time = ", (stop_time - start_time))
