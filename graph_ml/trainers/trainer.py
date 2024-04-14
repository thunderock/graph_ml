# Author: Ashutosh Tiwari
# Date: 4/14/24
# Project: GraphML
import numpy as np
import pytorch_lightning as pl
from ..utils import config

class Trainer(object):
    """
    takes a pl.LightningModule and trains it using the training paradigm
    can be Contrastive learning, supervised learning or any other learning paradigm
    """
    def __init__(self, model, **kwargs):
        self.model = model
        self.trainer = pl.Trainer(**kwargs)
        pl.seed_everything(config.SEED)
        self.tuning = config.TUNING
