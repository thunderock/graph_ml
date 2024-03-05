from __future__ import annotations

import pytest
from graph_ml import add

@pytest.mark.benchmark(group='add')
def test_add(benchmark):
    benchmark(add, 1, 2)