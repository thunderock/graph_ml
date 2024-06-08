from typing import Optional
import numpy as np
import pytorch_lightning as pl
import random
from ..utils import utils


class Sampler(object):
    def _set_seed(self):
        np.random.seed(self.seed)
        pl.seed_everything(self.seed)
        random.seed(self.seed)

    def _set_number_target(self, number_target):
        if number_target is None:
            self.number_target = number_target
        return self.number_target

    def __init__(self, window_length: int = 10, number_target: Optional[int] = None, seed: Optional[int] = None, degree_agnostic: Boolen) -> None:
        """
        Parameters
        ----------
        window_length : int
            Number of nodes to sample in the context window
        number_target : int
               Number of target nodes or edges to sample, can be none because fit can take centers
        seed : int
            Seed for random number generator
        """
        self.window_length = window_length
        self.number_target = number_target
        self.seed = utils.get_formatted_environ_variable("SEED", int, 42) if seed is None else seed
        self._set_seed()


    def num_nodes(self, A):
        return A.shape[0]

    def num_edges(self, A):
        return A.nnz

    def _generate_centers(self, A):
        return np.random.choice(self.num_nodes(A), self.number_target, replace=False)
    def sample(self, centers: Optional[np.ndarray], padding_mask: int = 0) -> np.ndarray:
        raise NotImplementedError


"""

Did:
1. Reviewed, tested and merged STD team's PR to fix principal failure issue.
2. Raised PR for funding type and reserve amount in ltd-cdf-pipeline.
3. Completed Pru backtesting and asked Drew to review.
4. Oncall deployment duties.
Will do:
1. Address any comments on PR for funding type and reserve amount in ltd-cdf-pipeline.
2. Start testing Prudential on ltd-raw-data-preprocessor.

Did:
1. Merged PR for funding type and reserve amount in ltd-cdf-pipeline.
2. Finished first version of Prudential on ltd-raw-data-preprocessor.
Will do:
1. Issue today for other clients due to funding type and reserve amount. Will check in local and then raise PR.
2. Keep working on Prudential on ltd-raw-data-preprocessor. I am stuck with how to use export date asset. Will reach out to platform oncall
in case not able to figure it out.
3. Postpartum meeting for oneamerica oncall issue. Ask questions I had in mind.
"""
