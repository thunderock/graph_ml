# Author: Ashutosh Tiwari
# Date: 3/19/24
# Project: GraphML
import numpy as np
from scipy import sparse
from ..utils import utils

class Sampler(object):
    """
    Base class for all samplers
    Every time there is a new adjacency matrix, sampler is required to be refitted.
    May be should be changed in future, fit to be allowed to called multiple times.
    """
    def __init__(self):
        pass

    def fit(self, ):