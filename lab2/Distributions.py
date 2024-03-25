  
from numpy.random import rayleigh, uniform, normal, exponential, weibull
from numpy.random import rayleigh
from scipy.stats import weibull_min
import random
import numpy as np

# Рэлея
class RayleighDistribution:
    def __init__(self, sigma: float):
        self.sigma = sigma

    def generate(self):
        return rayleigh(self.sigma)


# Равномерное
class UniformDistribution:
    def __init__(self, middle, range):
        self.a = middle - range
        self.b = middle + range

    def generate(self):
        return uniform(self.a, self.b)

# Нормальное
class NormalDistribution:
    def __init__(self, m: float, sigma: float):
        self.sigma = sigma
        self.m = m

    def generate(self):
        return normal(self.m, self.sigma)

# Экспотенциальное
class ExponentialDistribution:
    def __init__(self, lambda_param: float):
        self.lambda_param = lambda_param

    def generate(self):
        return exponential(1/self.lambda_param)

# Гаусса
class GaussDistribution:
    def __init__(self, m, sigma):
        self.m = m
        self.sigma = sigma

    def generation_time(self):
        return normal(self.m, self.sigma)
    

class WeibullDistribution:
    def __init__(self, k: float,lambd: float):
        self.k = k
        self.lam = lambd

    def generate(self):
        return weibull_min.rvs(self.k, loc=0, scale=self.lam)
    

