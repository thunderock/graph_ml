import numpy as np
import gensim
from ..utils import config, torch_utils

from ..models.node2vec import Node2Vec

class GensimNode2Vec(Node2Vec):
    def __init__(self, **params):
        super().__init__(**params)
        self.model_params = {
            "vector_size": self.embedding_dim,
            "window": self.context_size,
            "min_count": 0,
            "sg": 1,
            "hs": 0,
            "negative": 1,
            "ns_exponent": 0.5,
            "epochs": 1,
            "workers": self.num_workers
        }

