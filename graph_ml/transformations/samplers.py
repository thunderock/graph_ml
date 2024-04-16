# Author: Ashutosh Tiwari
# Date: 3/19/24
# Project: GraphML

import numpy as np
import torch
from ..utils import torch_utils, utils, config


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

    def fit(self, A):
        """
        Fit the sampler to the adjacency matrix
        Parameters
        ----------
        A : np.ndarray
            Adjacency matrix
        """
        self.n_nodes = A.shape[0]
        if self.group_membership is None:
            self.group_membership = np.zeros(self.n_nodes, dtype=np.int32)
        self.node2group = utils.to_member_matrix(self.group_membership)

        indeg = A.sum(axis=0)