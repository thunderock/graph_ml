# Author: Ashutosh Tiwari
# Date: 4/14/24
# Project: GraphML
from ..utils import config


class Trainer(object):
    """
    takes a torch module and trains it using the training paradigm
    can be Contrastive learning, supervised learning or any other learning paradigm
    """

    def __init__(self, model, **kwargs):
        self.model = model
        self.tuning = config.TUNING
