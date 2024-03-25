from Modeller import Modeller
from EventGenerator import Generator
from Distributions import  *
from Processor import Processor
import math
from matplotlib import pyplot

# def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr): 
#     sigma = (1/lambda_coming) * (math.pi / 2) ** (-1/2)

#     k = 2
#     lam = (1/lambda_obr) * math.log(2, math.e) ** (-1 / k)

#     generators = [
#         Generator(
#             ExpDistribution(sigma),
#             clients_number,
#         ), 
#     ]

#     operators = [
#             Processor(
#                 WeibullDistribution(k, lam)
#             ),
#         ]
#     for generator in generators: 
#         generator.receivers = operators.copy()

#     model = Modeller(generators, operators)
#     result = model.event_mode(clients_proccessed)
#     print("Загрузка системы(расчетная): ", lambda_coming/lambda_obr, 
#     "\nВремя работы:", result['time'], 
#     "\nСреднее время ожидания: ", result['wait_time_middle'], 
#     "\nКоличество обработанных заявок", clients_proccessed)
#     return result

# def modelling(num_requests, generator_intensity, generator_range, processor_intensity, processor_range):
def modelling(clients_number, clients_proccessed, lambda_coming, lambda_obr):

    k = 2
    lam = (1/lambda_obr) * math.log(2, math.e) ** (-1 / k)

    generators = [
        Generator(
            ExponentialDistribution(lambda_coming),
            clients_number
            #RayleighDistribution(sigma),
            #ExponentialDistribution(lambda_p)
        ),]

    ## ------------------------------------
    #mean = processor_intensity * math.sqrt(math.pi / 2)
    #sigma = 1 / mean

    operators = [
        Processor(
            #UniformDistribution(middle, range)
            #RayleighDistribution(sigma)
            WeibullDistribution(k, lam)
        ),]

    for generator in generators:
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(clients_proccessed)
    print("Загрузка системы(расчетная): ", lambda_coming/lambda_obr, 
    "\nВремя работы:", result['time'], 
    "\nСреднее время ожидания: ", result['wait_time_middle'], 
    "\nКоличество обработанных заявок", clients_proccessed)
    return result


def view(start, end, N):
    print(start, end, N)
    Xdata = list()
    Ydata = list()

    lambda_obr = 100
    k = 2

    for lambda_coming in range(int(start * 100), int(end * 100), 5):
            result = modelling(
                clients_number=N+1000,
                clients_proccessed=N, 
                lambda_coming=lambda_coming,
                lambda_obr=lambda_obr
            )
            Xdata.append(lambda_coming/lambda_obr)
            Ydata.append(result['wait_time_middle'])

    pyplot.title('Среднее время ожидания')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Коэффикиент загрузки")
    pyplot.ylabel("Среднее время пребывания в очереди")
    pyplot.show()