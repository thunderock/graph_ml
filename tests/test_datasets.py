from graph_ml.datasets import dataset, polbooks

polbooks = polbooks.PolBooks()


def test_type():
    assert isinstance(polbooks, dataset.Dataset)


def test_data_df():
    assert polbooks.data.shape[0] == 105
