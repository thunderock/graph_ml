# Author: Ashutosh Tiwari
# Date: 3/19/24
# Project: GraphML

# TODO(Ashutosh): rename everything to node_sampler instead of sampler
# TODO(Ashutosh): add type hints to all functions
# TODO(Ashutosh): add torch support to all functions

import numpy as np
from scipy import sparse
from ..utils import utils


class Sampler(object):
    """
    Base class for all samplers
    Every time there is a new adjacency matrix, sampler is required to be refitted.
    May be should be changed in future, fit to be allowed to called multiple times.
    """

    def fit(
        self, A
    ):
        raise NotImplementedError

    def sample(self, centers, contexts, padding_mask=None):
        raise NotImplementedError


class SbmNodeSampler(Sampler):
    def __init__(self, window_length=10, group_membership=None, dcsbm=True):
        """
        Parameters
        ----------
        window_length : int
            Number of nodes to sample in the context window
        group_membership : np.ndarray
            Group membership of each node
        dcsbm : bool
            sampling to take degree corrected sbm or not
        """
        self.window_length = window_length
        self.dcsbm = dcsbm
        self.group_membership = group_membership
        assert self.dcsbm, "Only dcsbm is supported"

    def fit(self, A):
        """
        Fit the sampler to the adjacency matrix
        Parameters
        ----------
        A : np.ndarray
            Adjacency matrix
        """
        print("type A ", type(A), A)
        self.n_nodes = A.shape[0]
        if self.group_membership is None:
            self.group_membership = np.zeros(self.n_nodes, dtype=np.int32)
        self.node2group = utils.to_member_matrix(self.group_membership)

        indeg = A.sum(axis=0)
        Lambda = (self.node2group.T @ A @ self.node2group).toarray()
        Din = Lambda.sum(axis=1)
        Nin = self.node2group.sum(axis=0)
        Psbm = np.einsum(
            "ij,i->ij", Lambda, 1 / np.maximum(1, Lambda.sum(axis=1))
        )
        Psbm_pow = utils.matrix_sum_power(Psbm, self.window_length) / self.window_length
        if self.dcsbm:
            self.block2node = (
                    sparse.diags(1 / np.maximum(1, Din))
                    @ sparse.csr_matrix(self.node2group.T)
                    @ sparse.diags(indeg)
            )
        self.block2block = sparse.csr_matrix(Psbm_pow)
        self.block2block.data = utils.csr_row_cumsum(
            self.block2block.indptr, self.block2block.data
        )
        self.block2node.data = utils.csr_row_cumsum(
            self.block2node.indptr, self.block2node.data
        )
        return self

    def sample(self, centers, contexts, padding_mask):
        block_ids = utils.sample_csr(
            self.group_membership[centers], self.block2block
        )
        context = utils.sample_csr(block_ids, self.block2node)
        return context.astype(np.int64)