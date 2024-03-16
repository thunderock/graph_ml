import pandas as pd
import networkx as nx
from torch_geometric.data import extract_zip


from ..datasets import dataset


class PolBooks(dataset.Dataset):

    def __init__(self, root: str = "/tmp/"):
        super().__init__(root=root, group_col="political_leaning",
                         urls=["https://websites.umich.edu/~mejn/netdata/polbooks.zip"])

    def _set_data_df(self):
        extract_zip(self.file_paths[0], self.root)
        self.graph = nx.read_gml(self.root + "polbooks.gml")
        node_dict = dict(self.graph.nodes(data=True))
        df = pd.DataFrame.from_dict(node_dict, orient='index').reset_index(drop=True). \
            rename(columns={'value': 'political_leaning'})
        df['political_leaning'] = df['political_leaning'].map(
            {'n': 0, 'c': 1, 'l': 2}
        )
        return df

    def _set_adj(self):
        return nx.adjacency_matrix(self.graph)
        pass