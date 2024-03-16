import numpy as np
from torch_geometric.nn import Node2Vec as PyGNode2Vec
import torch
from ..models.node2vec import Node2Vec
from ..utils import torch_utils


class TorchNode2Vec(Node2Vec):
    def __init__(self, **params):
        super().__init__(**params)
        self.model = PyGNode2Vec(
            edge_index=self.edge_index,
            embedding_dim=self.embedding_dim,
            walk_length=self.walk_length,
            context_size=self.context_size,
            sparse=True,
            **params,
        ).to(self.device)
        self.loader = self.optimizer = None

    @property
    def edge_index(self):
        # should not be called too often, no caching here
        return torch_utils.adj_list_to_edge_index(self.adj_list)

    def _fit(self, epochs, learning_rate, batch_size, shuffle=True):
        # TODO (ashutosh): check if training two times works
        self.loader = self.model.loader(
            batch_size=batch_size, shuffle=shuffle, num_workers=self.num_workers
        )
        self.optimizer = torch.optim.SparseAdam(
            self.model.parameters(), lr=learning_rate
        )
        self.model.train()
        total_loss = [0] * epochs
        for epoch in range(epochs):
            for pos_rw, neg_rw in self.loader:
                self.optimizer.zero_grad()
                loss = self.model.loss(
                    pos_rw.to(self.model.device), neg_rw.to(self.device)
                )
                loss.backward()
                self.optimizer.step()
                total_loss[epoch] += loss.item()
            total_loss[epoch] /= len(self.loader)
            if self.logging:
                print(f"Epoch: {epoch}, Loss: {total_loss[epoch]}")
        return self

    def _transform(self, nodes=None, type_=np.ndarray):
        self.model.eval()
        if nodes is None:
            nodes = torch.arange(self.num_nodes, device=self.device)
        with torch.no_grad():
            emb = self.model(torch.tensor(nodes, device=self.device)).detach()
        if type_ is np.ndarray:
            return emb.cpu().numpy()
        return emb
