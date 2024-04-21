from Modeller import Modeller
from EventGenerator import Generator
from Distributions import  *
from Processor import Processor
import math
from matplotlib import pyplot
from numpy import arange 

def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr, lambda_coming2=None, lambda_obr2=None): 
    k = 2
    lam = (1/lambda_obr) * math.log(2, math.e) ** (-1 / k)
    lam2 = lam
    if lambda_obr2:
        lam2 = (1/lambda_obr2) * math.log(2, math.e) ** (-1 / k)

    lambda1 = lambda_coming
    lambda2 = lambda1
    if lambda_coming2:
         lambda2 = lambda_coming2

    generators = [
        Generator(
            ExponentialDistribution(lambda1),
            clients_number,
            0
        ), 
        Generator(
            ExponentialDistribution(lambda2),
            clients_number,
            1
        ), 
    ]

    operators = [
            Processor(
                [WeibullDistribution(k, lam),
                WeibullDistribution(k, lam2)] 
            ),
        ]
    for generator in generators: 
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_proccessed)
    # print("Загрузка системы(расчетная): ", lambda_coming/lambda_obr, 
    # "\nВремя работы:", result['time'], 
    # "\nСреднее время ожидания: ", result['wait_time_middle'], 
    # "\nКоличество обработанных заявок", clients_proccessed)
    return result


def view(start, end, N):
    print(start, end, N)
    Xdata = list()
    Ydata = list()

    lambda_obr = 100
    k = 2

    for lambda_coming in arange(int(start * 100), int(end * 100)/2, 1):
            result = modelling(
                clients_number=N+1000,
                clients_proccessed=N, 
                lambda_coming=lambda_coming,
                lambda_obr=lambda_obr
            )
            Xdata.append(lambda_coming*2/lambda_obr)
            Ydata.append(result['wait_time_middle'])

    pyplot.title('Среднее время ожидания')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Коэффициент загрузки")
    pyplot.ylabel("Среднее время пребывания в очереди")
    pyplot.show()

def norm_to_nat_pfe(xm, xd, b):
    m, d = xm, xd
    delta_x = d
    average_x = m
    b_denorm = np.array(b)
    b_denorm[0] /= 1
    b_denorm[1] /= delta_x[1]
    b_denorm[2] /= delta_x[2]
    b_denorm[3] /= delta_x[3]
    b_denorm[4] /= delta_x[4]
    b_denorm[5] /= delta_x[1] * delta_x[2]
    b_denorm[6] /= delta_x[1] * delta_x[3]
    b_denorm[7] /= delta_x[1] * delta_x[4]
    b_denorm[8] /= delta_x[2] * delta_x[3]
    b_denorm[9] /= delta_x[2] * delta_x[4]
    b_denorm[10] /= delta_x[3] * delta_x[4]
    b_denorm[11] /= delta_x[1] * delta_x[2] * delta_x[3]
    b_denorm[12] /= delta_x[1] * delta_x[2] * delta_x[4]
    b_denorm[13] /= delta_x[1] * delta_x[3] * delta_x[4]
    b_denorm[14] /= delta_x[2] * delta_x[3] * delta_x[4]
    b_denorm[15] /= delta_x[1] * delta_x[2] * delta_x[3] * delta_x[4]
    hash_table = {(1): 1, (2): 2, (3): 3, (4): 4, (1, 2): 5, (1, 3): 6, (1, 4): 7, (2, 3): 8, (2, 4): 9, (3, 4): 10, (1, 2, 3): 11, (1, 2, 4): 12, (1, 3, 4): 13, (2, 3, 4): 14, (1, 2, 3, 4): 15}
    b_natural = b_denorm.copy()
    # 0-взаимодействие
    for i in range(1, len(delta_x)):
        b_natural[0] -= b_denorm[hash_table[(i)]] * average_x[i]
    
    # 1-взаимодействие
    for i in range(1, len(delta_x)):
        for j in range(i + 1, len(delta_x)):
            b_natural[0] += b_denorm[hash_table[(i, j)]] * average_x[i] * average_x[j]
            b_natural[hash_table[(i)]] -= b_denorm[hash_table[(i, j)]] * average_x[j]
            b_natural[hash_table[(j)]] -= b_denorm[hash_table[(i, j)]] * average_x[i]
    
    # 2-взаимодействие
    for i in range(1, len(delta_x)):
        for j in range(i + 1, len(delta_x)):
            for k in range(j + 1, len(delta_x)):
                b_natural[0] -= b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[j] * average_x[k]
                b_natural[hash_table[(i)]] += b_denorm[hash_table[(i, j, k)]] * average_x[j] * average_x[k]
                b_natural[hash_table[(j)]] += b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[k]
                b_natural[hash_table[(k)]] += b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[j]
                b_natural[hash_table[(i, j)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[k]
                b_natural[hash_table[(i, k)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[j]
                b_natural[hash_table[(j, k)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[i]
    
    # 3-взаимодействие
    b_natural[0] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[2] * average_x[3] * average_x[4]
    b_natural[hash_table[(1)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[2] * average_x[3] * average_x[4]
    b_natural[hash_table[(2)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[3] * average_x[4]
    b_natural[hash_table[(3)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[2] * average_x[4]
    b_natural[hash_table[(4)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[2] * average_x[3]
    b_natural[hash_table[(1, 2)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[3] * average_x[4]
    b_natural[hash_table[(1, 3)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[2] * average_x[4]
    b_natural[hash_table[(1, 4)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[2] * average_x[3]
    b_natural[hash_table[(2, 3)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[4]
    b_natural[hash_table[(2, 4)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[3]
    b_natural[hash_table[(3, 4)]] += b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1] * average_x[2]
    b_natural[hash_table[(1, 2, 3)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[4]
    b_natural[hash_table[(1, 2, 4)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[3]
    b_natural[hash_table[(1, 3, 4)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[2]
    b_natural[hash_table[(2, 3, 4)]] -= b_denorm[hash_table[(1, 2, 3, 4)]] * average_x[1]

    return b_natural


def norm_to_nat_dfe(xm, xd, b):
    m, d = xm, xd
    delta_x = d
    average_x = m
    n = 3
    b_denorm = np.array(b[:5 + n] + [0] + b[5 + n:])

    b_denorm[0] /= 1
    b_denorm[1] /= delta_x[1]
    b_denorm[2] /= delta_x[2]
    b_denorm[3] /= delta_x[3]
    b_denorm[4] /= delta_x[4]
    b_denorm[5] /= delta_x[1] * delta_x[2]
    b_denorm[6] /= delta_x[1] * delta_x[3]
    b_denorm[7] /= delta_x[2] * delta_x[3]
    b_denorm[8] /= delta_x[1] * delta_x[2] * delta_x[3]
    lst = [(1, 2), (1, 3), (2, 3), (1, 2, 3)]
    hash_table = {(1): 1, (2): 2, (3): 3, (4): 4, (1, 2): 5, (1, 3): 6, (2, 3): 7, (1, 2, 3): 8}
    b_natural = b_denorm.copy()
    # 0-взаимодействие
    for i in range(1, len(delta_x)):
        b_natural[0] -= b_denorm[hash_table[(i)]] * average_x[i]
    
    # 1-взаимодействие
    for interaction in lst[:3]:
        i, j = interaction
        b_natural[0] += b_denorm[hash_table[(i, j)]] * average_x[i] * average_x[j]
        b_natural[hash_table[(i)]] -= b_denorm[hash_table[(i, j)]] * average_x[j]
        b_natural[hash_table[(j)]] -= b_denorm[hash_table[(i, j)]] * average_x[i]
    
    # 2-взаимодействие
    i, j, k = (1, 2, 3)
    b_natural[0] -= b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[j] * average_x[k]
    b_natural[hash_table[(i)]] += b_denorm[hash_table[(i, j, k)]] * average_x[j] * average_x[k]
    b_natural[hash_table[(j)]] += b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[k]
    b_natural[hash_table[(k)]] += b_denorm[hash_table[(i, j, k)]] * average_x[i] * average_x[j]
    b_natural[hash_table[(i, j)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[k]
    b_natural[hash_table[(i, k)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[j]
    b_natural[hash_table[(j, k)]] -= b_denorm[hash_table[(i, j, k)]] * average_x[i]

    return b_natural


def norm_to_nat_dfe_lin(xm, xd, b):
    m, d = xm, xd

    a = [0 for i in range(5)]

    s = 0
    for i in range(1,5):
        s += b[i] * m[i] / d[i]

    a[0] += b[0] - s

    for i in range(1, 5):
        a[i] = b[i] / d[i]

    return a