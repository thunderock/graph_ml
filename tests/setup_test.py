from __future__ import annotations

import pytest
from graph_ml import add


def test_add():
    assert add(1, 2) == 3
    pytest.raises(TypeError, add, 1, "2")
