import pytest

from graph_ml.datasets import polbooks
from graph_ml.transformations import samplers


@pytest.fixture()
def dataset():
    return polbooks.PolBooks()


def test_sbm_node_sampler(dataset):
    sampler = samplers.SbmNodeSampler(group_membership=dataset.y, window_length=10).fit(
        dataset.adj
    )
    assert sampler.block2block.shape == (3, 3)
    assert sampler.block2node.shape == (3, 105)
    assert sampler.node2group.shape == (105, 3)
