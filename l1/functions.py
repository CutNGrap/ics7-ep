import math

from matplotlib import pyplot
import numpy as np

from Distributions import *
from EventGenerator import Generator
from Modeller import Modeller
from Processor import Processor

REPEATS_COUNT = 100

def modelling(num_requests, generator_intensity, generator_range, processor_intensity, processor_range):
    mean = generator_intensity * math.sqrt(math.pi / 2)
    sigma = 1 / mean

    lambda_p = generator_intensity

    middle = 1 / generator_intensity
    range = generator_range
    if middle - range <= 0:
        raise ValueError(
            "Разница мат. ожидания и разброса должна быть больше нуля")

    k = 2
    lam = (1/processor_intensity) * math.log(2, math.e) ** (-1 / k)

    generators = [
        Generator(
            ExponentialDistribution(lambda_p)
            #RayleighDistribution(sigma),
            #ExponentialDistribution(lambda_p)
        ),]

    ## ------------------------------------
    #mean = processor_intensity * math.sqrt(math.pi / 2)
    #sigma = 1 / mean

    lambda_p = processor_intensity

    middle = 1 / processor_intensity
    range = processor_range
    if middle - range <= 0:
        raise ValueError(
            "Разница мат. ожидания и разброса должна быть больше нуля")

    operators = [
        Processor(
            #UniformDistribution(middle, range)
            #RayleighDistribution(sigma)
            WeibullDistribution(k, lam)
        ),]

    for generator in generators:
        generator.receivers = operators.copy()

    model = Modeller(generators, operators)
    result = model.event_mode(num_requests)
    return result


def view_generator_intensity(start, end, N):
    Xdata = list()
    Ydata = list()

    processor_intensity = 30

    for generator_intensity in range(start, end, 1):
        print("generator_intensity = {}".format(generator_intensity))
        mean_time_in_queue = []
        for _ in range(REPEATS_COUNT):
            result = modelling(
                num_requests=N,
                generator_intensity=generator_intensity,
                processor_intensity=processor_intensity,
                generator_range=0,
                processor_range=0
            )
            mean_time_in_queue.append(result['mean_time_in_queue'])

        Xdata.append(generator_intensity)
        Ydata.append(sum(mean_time_in_queue) / len(mean_time_in_queue))

    pyplot.title('Зависимость от интенсивности генерации')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Интенсивность генерации")
    pyplot.ylabel("Среднее время ожидания")
    pyplot.show()


def view_processor_intensity(start, end, N):
    Xdata = list()
    Ydata = list()

    generator_intensity = 1

    for processor_intensity in np.arange(start, end, 0.5):
        print("processor_intensity = {}".format(processor_intensity))
        mean_time_in_queue = []
        for _ in range(REPEATS_COUNT):
            result = modelling(
                num_requests=N,
                generator_intensity=generator_intensity,
                processor_intensity=processor_intensity,
                generator_range=0,
                processor_range=0
            )
            mean_time_in_queue.append(result['mean_time_in_queue'])

        Xdata.append(processor_intensity)
        Ydata.append(sum(mean_time_in_queue) / len(mean_time_in_queue))

    pyplot.title('Зависимость от интенсивности обслуживания')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Интенсивность обслуживания")
    pyplot.ylabel("Среднее время ожидания")
    pyplot.show()


def view_workload(start, end, N):
    Xdata = list()
    Ydata = list()

    processor_intensity = 100

    for generator_intensity in range(int(start * 100), int(end * 100), 5):
        print("generator_intensity = {}".format(generator_intensity))
        mean_time_in_queue = []
        for _ in range(REPEATS_COUNT):
            result = modelling(
                num_requests=N,
                generator_intensity=generator_intensity,
                processor_intensity=processor_intensity,
                generator_range=0,
                processor_range=0
            )
            mean_time_in_queue.append(result['mean_time_in_queue'])

        Xdata.append(generator_intensity/processor_intensity)
        Ydata.append((sum(mean_time_in_queue) / len(mean_time_in_queue))* 100)

    pyplot.title('Зависимость от загрузки СМО')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Коэффициент загрузки СМО")
    pyplot.ylabel("Среднее время ожидания")
    pyplot.show()
