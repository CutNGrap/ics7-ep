import random
import math
import numpy.random as nr
from scipy.stats import weibull_min


def gauss_t(params):
    mx = params[0]
    dx = params[1]
    
    return nr.normal(mx, dx)

def exponent_t(param):
    return nr.exponential(param[0])

def weibull_t(param):
    return weibull_min.rvs(2, loc=0, scale=param[0])

