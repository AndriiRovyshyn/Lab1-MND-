import random
import numpy as np
import math

var = 319
m = 5

ymax = (30 - var) * 10
ymin = (20 - var) * 10
x1min = -20
x1max = 30
x2min = 20
x2max = 60

mtrx = [[-1, -1], [1, -1], [-1, 1]]  # матриця планування

Y = [[random.randint(ymin, ymax) for i in range(m)] for j in range(3)]  # функція відгуку
print(f"Матриця планування при m = {m}:")
for i in range(3):
    print(Y[i])

Y_average = []
for i in range(len(Y)):
    Y_average.append(np.mean(Y[i]))

dispersions = []
for i in range(len(Y)):
    sum = 0
    for k in Y[i]:
        sum += (k - np.mean(Y[i])) ** 2
    dispersions.append(sum / len(Y[i]))
print("Дисперсії:", dispersions)


def determinant(x11, x12, x13, x21, x22, x23, x31, x32, x33):
    deter = x11 * x22 * x33 + x12 * x23 * x31 + x32 * x21 * x13 - x13 * x22 * x31 - x32 * x23 * x11 - x12 * x21 * x33
    return deter


# --------------------------Перевірка однорідності дисперсії за критерієм Романовського---------------------------------
sigma_teta = math.sqrt((2 * (2 * m - 2)) / (m * (m - 4)))

dis = [max(dispersions[0], dispersions[1]) / min(dispersions[0], dispersions[1]),
       max(dispersions[2], dispersions[0]) / min(dispersions[2], dispersions[0]),
       max(dispersions[2], dispersions[1]) / min(dispersions[2], dispersions[1])]

teta = [((m - 2) / m) * dis[0], ((m - 2) / m) * dis[1], ((m - 2) / m) * dis[2]]

mod = [abs(teta[0] - 1) / sigma_teta, abs(teta[1] - 1) / sigma_teta, abs(teta[2] - 1) / sigma_teta]
print("Експериментальні значення критерію Романовського:")
for i in range(3):
    print(mod[i])

r_kr = 2
for i in range(len(mod)):
    if mod[i] > r_kr:
        print("Неоднорідна дисперсія")


mx1 = (mtrx[0][0] + mtrx[1][0] + mtrx[2][0]) / 3
mx2 = (mtrx[0][1] + mtrx[1][1] + mtrx[2][1]) / 3
my = (Y_average[0] + Y_average[1] + Y_average[2]) / 3

a1 = (mtrx[0][0] ** 2 + mtrx[1][0] ** 2 + mtrx[2][0] ** 2) / 3
a2 = (mtrx[0][0] * mtrx[0][1] + mtrx[1][0] * mtrx[1][1] + mtrx[2][0] * mtrx[2][1]) / 3
a3 = (mtrx[0][1] ** 2 + mtrx[1][1] ** 2 + mtrx[2][1] ** 2) / 3
a11 = (mtrx[0][0] * Y_average[0] + mtrx[1][0] * Y_average[1] + mtrx[2][0] * Y_average[2]) / 3
a22 = (mtrx[0][1] * Y_average[0] + mtrx[1][1] * Y_average[1] + mtrx[2][1] * Y_average[2]) / 3

b0 = determinant(my, mx1, mx2, a11, a1, a2, a22, a2, a3) / determinant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)
b1 = determinant(1, my, mx2, mx1, a11, a2, mx2, a22, a3) / determinant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)
b2 = determinant(1, mx1, my, mx1, a1, a11, mx2, a2, a22) / determinant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)

# коефіцієнти нормованих рівнянь регресії
yNorm1 = b0 + b1 * mtrx[0][0] + b2 * mtrx[0][1]
yNorm2 = b0 + b1 * mtrx[1][0] + b2 * mtrx[1][1]
yNorm3 = b0 + b1 * mtrx[2][0] + b2 * mtrx[2][1]

dx1 = abs(x1max - x1min) / 2
dx2 = abs(x2max - x2min) / 2
x10 = (x1max + x1min) / 2
x20 = (x2max + x2min) / 2

a_0 = b0 - (b1 * x10 / dx1) - (b2 * x20 / dx2)
a_1 = b1 / dx1
a_2 = b2 / dx2

# натуралізація рівняння регресії
yNat1 = a_0 + a_1 * x1min + a_2 * x2min
yNat2 = a_0 + a_1 * x1max + a_2 * x2min
yNat3 = a_0 + a_1 * x1min + a_2 * x2max

print("Середні значення:", Y_average[0], Y_average[1], Y_average[2])
print("Нормовані коефіцієнти:", round(yNorm1, 4), round(yNorm2, 4), round(yNorm3, 4))
print("Натуралізовані коефіцієнти:", round(yNat1, 4), round(yNat2, 4), round(yNat3, 4))