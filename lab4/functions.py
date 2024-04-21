from Modeller import Modeller
from EventGenerator import Generator
from Distributions import  RayleighDistribution, WeibullDistribution
from Processor import Processor
import math
from matplotlib import pyplot
from numpy import arange 
import numpy as np

def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr, lambda_coming2=None, lambda_obr2=None): 
    sigma = (1/lambda_coming) * (math.pi / 2) ** (-1/2)
    sigma2 = sigma 
    if lambda_coming2: 
        sigma2 = (1/lambda_coming2) * (math.pi / 2) ** (-1/2)


    k = 2
    lam = (1/lambda_obr) * math.log(2, math.e) ** (-1 / k)
    lam2 = lam 
    if lambda_obr2:
        lam2 = (1/lambda_obr2) * math.log(2, math.e) ** (-1 / k)

    generators = [
        Generator(
            RayleighDistribution(sigma),
            clients_number,
            0
        ), 
        Generator(
            RayleighDistribution(sigma2),
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


def norm_to_nat_dfe(xm, xd, b):
    m, d = xm, xd
    delta_x = d
    average_x = m
    n = 3
    b_denorm = np.array(b[:5 + n] + b[5 + n:])

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
    b_denorm[11] /= delta_x[1] ** 2
    b_denorm[12] /= delta_x[2] ** 2
    b_denorm[13] /= delta_x[3] ** 2
    b_denorm[14] /= delta_x[4] ** 2
    hash_table = {(1): 1, (2): 2, (3): 3, (4): 4, (1, 2): 5, (1, 3): 6, (1, 4): 7, (2, 3): 8, (2, 4): 9, (3, 4): 10, (1, 1): 11, (2, 2): 12, (3, 3): 13, (4, 4): 14}
    b_natural = b_denorm.copy()
    # 0-взаимодействие
    for i in range(1, len(delta_x)):
        b_natural[0] -= b_denorm[hash_table[(i)]] * average_x[i]
    
    # 1-взаимодействие
    for i in range(1, len(delta_x)):
        for j in range(i, len(delta_x)):
            b_natural[0] += b_denorm[hash_table[(i, j)]] * average_x[i] * average_x[j]
            b_natural[hash_table[(i)]] -= b_denorm[hash_table[(i, j)]] * average_x[j]
            b_natural[hash_table[(j)]] -= b_denorm[hash_table[(i, j)]] * average_x[i]


    return b_natural