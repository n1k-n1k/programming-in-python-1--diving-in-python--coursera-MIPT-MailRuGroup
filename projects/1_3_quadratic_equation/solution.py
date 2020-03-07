'''
Корни квадратного уравнения

Yаписать программу, которая запускается в командной строке с параметрами,
вычисляет значения корней квадратного уравнения и выводит их на печать.
На вход программе подаются коэффициенты a, b и c.
На печать должно выводиться два корня квадратного уравнения.
Обратите внимание на то, как выводятся корни - каждый с новой строки.

Чтобы не усложнять вашу задачу все коэффициенты,
которые мы будем подавать вам на вход являются коэффициентами,
которые в итоге дают 2 корня квадратного уравнения.

Корни должны быть приведены к целочисленному виду перед выводом на экран,
порядок вывода корней произвольный.
'''

import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

sqrt_D = (b ** 2 - 4 * a * c) ** 0.5
x1 = int(-(b + sqrt_D) / 2 / a)
x2 = int(-(b - sqrt_D) / 2 / a)

print(x1)
print(x2)
