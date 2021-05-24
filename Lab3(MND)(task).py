import numpy as np
import random
from prettytable import PrettyTable
import pandas as pd
import sys
from scipy.stats import f, t
from functools import partial

n = 4
m = 4
f1 = m - 1
f2 = n
f3 = f1 * f2
q = 0.05

# 1 пункт
print("1.Лінійне рівняння: \n y^ = b0 + b1 * x1 + b2 * x2 + b3 * x3")
print()

# 2 пунктт
plan_matrix = [[1, -1, -1, -1],
               [1, -1, 1, 1],
               [1, 1, -1, 1],
               [1, 1, 1, -1]]

print("2.Матриця планування експерименту:")
table1 = PrettyTable()
table1.field_names = ["№", "-x0", "-x1", "-x2", "-x3"]
table1.add_rows([
    ["1", plan_matrix[0][0], plan_matrix[0][1], plan_matrix[0][2], plan_matrix[0][3]],
    ["2", plan_matrix[1][0], plan_matrix[1][1], plan_matrix[1][2], plan_matrix[1][3]],
    ["3", plan_matrix[2][0], plan_matrix[2][1], plan_matrix[2][2], plan_matrix[2][3]],
    ["4", plan_matrix[3][0], plan_matrix[3][1], plan_matrix[3][2], plan_matrix[3][3]]
])
print(table1)

# 3 пункт
x1_min = -20
x1_max = 30
x2_min = 20
x2_max = 60
x3_min = -20
x3_max = -5
y_min, y_max = int(200 + (x1_min + x2_min + x3_min) / 3), int(200 + (x1_max + x2_max + x3_max) / 3)


def rnumbers(x1, x2):
    array = []
    for i in range(4):
        array.append(random.randint(x1, x2 + 1))
    return array


x0 = [1, 1, 1, 1]
x1 = rnumbers(x1_min, x1_max)
x2 = rnumbers(x2_min, x2_max)
x3 = rnumbers(x3_min, x3_max)
y1 = rnumbers(y_min, y_max)
y2 = rnumbers(y_min, y_max)
y3 = rnumbers(y_min, y_max)

print("3.Матриця планування з натуралізованими значеннями факторів:")
table2 = PrettyTable()
table2.field_names = ["X1", "X2", "X3", "Y1", "Y2", "Y3"]
for i in range(len(x1)):
    table2.add_row([x1[i], x2[i], x3[i], y1[i], y2[i], y3[i]])
print(table2)

# 4 пункт
print("4.Середні значення функції відгуку за рядками:")
y_avrg = []
for i in range(len(y1)):
    y_avrg.append(round((y1[i] + y2[i] + y3[i]) / 3, 4))
print("Y1 average: ", y_avrg[0])
print("Y2 average: ", y_avrg[1])
print("Y3 average: ", y_avrg[2])
print("Y4 average: ", y_avrg[3])
print()

mx_arr = [round(sum(x1) / 4, 1), round(sum(x2) / 4, 1), round(sum(x3) / 4, 4)]
print("mx1: ", mx_arr[0])
print("mx2: ", mx_arr[1])
print("mx3: ", mx_arr[2])
print()

my = round(np.average(y_avrg), 4)
print("my: ", my)
print()

a_arr = []
for i in range(3):
    a = 0
    for j in range(4):
        a += globals()["x" + str(i + 1)][j] * y_avrg[j]
    a_arr.append(round(a / 4, 4))
print("a1: ", a_arr[0])
print("a2: ", a_arr[1])
print("a3: ", a_arr[2])
print()

aa_arr = []
for i in range(3):
    a = 0
    for j in range(4):
        a += globals()["x" + str(i + 1)][j] ** 2
    aa_arr.append(round(a / 4, 4))

a12 = 0
a13 = 0
a23 = 0
for j in range(4):
    a12 += x1[j] * x2[j]
for j in range(4):
    a13 += x1[j] * x3[j]
for j in range(4):
    a23 += x2[j] * x3[j]

a12 = a21 = round(a12 / 4, 4)
a13 = a31 = round(a13 / 4, 4)
a23 = a32 = round(a23 / 4, 4)

a_matrix = [[aa_arr[0], a12, a13],
            [a21, aa_arr[1], a23],
            [a31, a32, aa_arr[2]]]

print("a_matrix: ")
print(pd.DataFrame(a_matrix, columns=list('123'), index=list('123')))
print()

b0 = round(np.linalg.det([[my, mx_arr[0], mx_arr[1], mx_arr[2]],
                          [a_arr[0], aa_arr[0], a12, a13],
                          [a_arr[1], a12, aa_arr[1], a32],
                          [a_arr[2], a13, a23, aa_arr[2]]]) / np.linalg.det(
    [[1, mx_arr[0], mx_arr[1], mx_arr[2]],
     [mx_arr[0], aa_arr[0], a12, a13],
     [mx_arr[1], a12, aa_arr[1], a32],
     [mx_arr[2], a13, a23, aa_arr[2]]]), 4)

b1 = round(np.linalg.det([[1, my, mx_arr[1], mx_arr[2]],
                          [mx_arr[0], a_arr[0], a12, a13],
                          [mx_arr[1], a_arr[1], aa_arr[1], a32],
                          [mx_arr[2], a_arr[2], a23, aa_arr[2]]]) / np.linalg.det(
    [[1, mx_arr[0], mx_arr[1], mx_arr[2]],
     [mx_arr[0], aa_arr[0], a12, a13],
     [mx_arr[1], a12, aa_arr[1], a32],
     [mx_arr[2], a13, a23, aa_arr[2]]]), 4)

b2 = round(np.linalg.det([[1, mx_arr[0], my, mx_arr[2]],
                          [mx_arr[0], aa_arr[0], a_arr[0], a13],
                          [mx_arr[1], a12, a_arr[1], a32],
                          [mx_arr[2], a13, a_arr[2], aa_arr[2]]]) / np.linalg.det(
    [[1, mx_arr[0], mx_arr[1], mx_arr[2]],
     [mx_arr[0], aa_arr[0], a12, a13],
     [mx_arr[1], a12, aa_arr[1], a32],
     [mx_arr[2], a13, a23, aa_arr[2]]]), 4)

b3 = round(np.linalg.det([[1, mx_arr[0], mx_arr[1], my],
                          [mx_arr[0], aa_arr[0], a12, a_arr[0]],
                          [mx_arr[1], a12, aa_arr[1], a_arr[1]],
                          [mx_arr[2], a13, a23, a_arr[2]]]) / np.linalg.det(
    [[1, mx_arr[0], mx_arr[1], mx_arr[2]],
     [mx_arr[0], aa_arr[0], a12, a13],
     [mx_arr[1], a12, aa_arr[1], a32],
     [mx_arr[2], a13, a23, aa_arr[2]]]), 4)
print("Запишемо отримане рівняння регресії:")
print("у = ", b0, "+ (", b1, ") * x1 + (", b2, ") * x2 + (", b3, ") * x3")


def regression(x1, x2, x3):
    global b0, b1, b2, b3
    y = b0 + b1 * x1 + b2 * x2 + b3 * x3
    return round(y, 4)


print("Зробимо перевірку:")
for i in range(len(y_avrg)):
    print(regression(x1[i], x2[i], x3[i]), "=", y_avrg[i])
print("Значення збігаються. Існують невеличку розбіжності через округлення")
print()

# 5 пункт
print("5.Проведення статистичних перевірок")
s_array = []
for i in range(4):
    s = 0
    for j in range(3):
        s += (globals()["y" + str(j + 1)][i] - y_avrg[i]) ** 2
    s_array.append(round(s / 3, 4))
print("Дисперсія: ", s_array)
print()

gp = round(max(s_array) / sum(s_array), 4)
print("Gp: ", gp)

q1 = q / f1
fisher_value = f.ppf(q=1 - q1, dfn=f2, dfd=(f1 - 1) * f2)
G_kr = fisher_value / (fisher_value + f1 - 1)

if gp < G_kr:
    print("Дисперсія однорідна, можна продовжити експеримент.")
else:
    print("Неоднорідна дисперсія, повторіть експеримент.")
    sys.exit()
print()

print("Оцінимо значимість коефіцієнтів регресії згідно критерію Стьюдента")
s_b = round(sum(s_array) / 4, 4)
s_bs = round(s_b / 12, 4)
sqrt_sbs = round(np.sqrt(s_bs), 4)
print("S^2b: ", s_b)
print("S^2bs: ", s_bs)
print("Sqrt(S^2bs): ", sqrt_sbs)

beta = []
teta = []

for i in range(4):
    b = 0
    for j in range(4):
        b += y_avrg[j] * plan_matrix[j][i]
    beta.append(round(b / 4, 4))

for i in range(4):
    teta.append(round(abs(beta[i]) / sqrt_sbs, 4))

student = partial(t.ppf, q=1 - 0.025)
t_student = student(df=f3)

for i in range(len(teta)):
    if teta[i] > t_student:
        print(teta[i], "Входить в рівняння")
    else:
        print(teta[i], "Виключається з рівнняня")

koef_t = []
new_t = []
for i in range(len(teta)):
    if teta[i] > t_student:
        koef_t.append(i)

for i in range(4):
    t = 0
    for j in koef_t:
        t += globals()["b" + str(j)] * globals()["x" + str(j)][i]
    new_t.append(t)
print("Рівнняня:")

for i in koef_t:
    print("b" + str(i), "*", "x" + str(i), end=" ")
    print("+", end=" ")
print(0)
print("y1^, y2^, y3^, y4^: ", new_t)
print()

print("Критерій Фішера")
sad = 0
for i in range(4):
    sad += (new_t[i] - y_avrg[i]) ** 2
s_ad = round(sad * 1.5, 4)
fp = round(s_ad / s_bs, 4)
res = koef_t
d = len(res)
f4 = n - d
fisher = partial(f.ppf, q=1 - 0.05)
ft = fisher(dfn=f4, dfd=f3)

print("Sad: ", s_ad)
print("Ft: ", ft)
print("Fp: ", fp)
if fp > ft:
    print("Fp > Fт. \nОтже, рівняння регресії неадекватно оригіналу при рівні значимості 0.05")

print('----------------------------------------------------------------------------------------')

print("Використаємо scipy для пошуку коефіцієнтів для статистичних перевірок.")
print("Маємо:")
print("Коефіцієнт Кохрена: ", G_kr)
print("Коефіцієнт Стьюдента: ", t_student)
print("Коефіцієнт Фішера: ", ft)