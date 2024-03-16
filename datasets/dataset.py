from typing import List, Tuple

import pandas as pd
import scipy
from torch_geometric.data import download_url


class Dataset(object):
    def __init__(self, root: str = '/tmp/', group_col: str = None, urls: List = None) -> None:
        self.root = root
        self.group_col = group_col
        self.file_paths = []
        urls = urls or []
        for url in urls:
            self.file_paths.append(download_url(url, root))
        self.data = self._set_data_df()
        self.adj = self._set_adj()

    @property
    def X(self):
        return self.data.loc[:, self.data.columns != self.group_col].values

    @property
    def y(self):
        return self.data[:, self.group_col].values

    def _set_data_df(self) -> pd.DataFrame:
        raise NotImplementedError

    def _set_adj(self) -> scipy.sparse:
        raise NotImplementedError