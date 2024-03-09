import numpy as np
import torch
from torch_geometric.nn import Node2Vec as PyGNode2Vec


from ..utils import config, torch_utils


class Node2Vec(object):
    def __init__(self, adj_list, embedding_dim, walk_length, context_size, device=config.DEVICE,
                 logging=config.LOGGING, **params):
        edge_index = torch_utils.adj_list_to_edge_index(adj_list)
        self.model = PyGNode2Vec(
            edge_index, embedding_dim, walk_length, context_size, **params
        ).to(device)
        self.num_workers = config.WORKER_COUNT
        self.logging = logging
        self.loader = self.optimizer = None

    def fit(self, epochs=1, learning_rate=.1, batch_size=128):

        # TODO (ashutosh): check if training two times works
        self.loader = self.model.loader(
            batch_size=batch_size, shuffle=True, num_workers=self.num_workers
        )
        self.optimizer = torch.optim.SparseAdam(self.model.parameters(), lr=learning_rate)
        self.model.train()
        total_loss = [0] * epochs
        for epoch in range(epochs):
            for pos_rw, neg_rw in self.loader:
                self.optimizer.zero_grad()
                loss = self.model.loss(pos_rw.to(self.model.device), neg_rw.to(self.model.device))
                loss.backward()
                self.optimizer.step()
                total_loss[epoch] += loss.item()
            total_loss[epoch] /= len(self.loader)
            if self.logging:
                print(f"Epoch: {epoch}, Loss: {total_loss[epoch]}")
        return sum(total_loss) / epochs

    def transform(self, nodes=None, type_=np.ndarray):
        if nodes is None:
            nodes = torch.arange(self.model.num_nodes)
        if type_ is np.ndarray:
            return self.model(nodes).detach().cpu().numpy()
        return self.model(nodes).detach()

    def fit_transform(self, epochs=1, learning_rate=.1, batch_size=128, nodes=None, type_=np.ndarray):
        self.fit(epochs, learning_rate, batch_size)
        return self.transform(nodes, type_)









