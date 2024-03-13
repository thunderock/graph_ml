import numpy as np
import torch
from torch_geometric.nn import Node2Vec as PyGNode2Vec


from ..utils import config, torch_utils


class Node2Vec(object):
    def __init__(self, adj_list, embedding_dim, walk_length, context_size, device=config.DEVICE,
                 logging=config.LOGGING, **params):
        self.adj_list = adj_list
        self.num_workers = config.WORKER_COUNT
        self.logging = logging
        self.embedding_dim = embedding_dim
        self.walk_length = walk_length
        self.context_size = context_size
        self.device = device

    def fit(self, epochs=1, learning_rate=.1, batch_size=128):
        return self._fit(epochs, learning_rate, batch_size)

    def transform(self, nodes=None, type_=np.ndarray):
        return self._transform(nodes, type_)

    def fit_transform(self, epochs=1, learning_rate=.1, batch_size=128, nodes=None, type_=np.ndarray):
        self.fit(epochs, learning_rate, batch_size)
        return self.transform(nodes, type_)









