import pandas as pd
import networkx as nx


from datasets import dataset


class PolBlogs(dataset.Dataset):

    def __init__(self, root: str = "/tmp/"):
        super().__init__(root=root, group_col="political_leaning",
                         urls=["https://websites.umich.edu/~mejn/netdata/polbooks.zip"])

    def _set_data_df(self):
        pass

    def _set_adj(self):
        pass