from graph_ml import CyTrie
import pytest

import pytest


@pytest.fixture()
def ca_words():
    return ["cat", "car", "cartoon", "carate"]


@pytest.fixture()
def ta_words():
    return ["tabla", "table", "taboo"]


@pytest.fixture()
def words(ta_words, ca_words):
    return ta_words + ca_words


def test_find(words):
    trie = CyTrie()
    trie.extend(words)
    for word in words:
        assert word in trie

    assert "rofl" not in trie


def test_prefix_not_in_trie():
    trie = CyTrie()
    assert "ca" not in trie


def test_len(words):
    trie = CyTrie()
    trie.extend(words)
    assert len(trie) == len(words)


def test_iter(words):
    trie = CyTrie(words)
    trie.extend(words)
    assert sorted(trie) == sorted(words)




@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2, ["cat", "cartoon", "car"]),
        (["cat"] * 2 + ["car"] * 1 + ["cartoon"] * 3, ["cartoon", "cat", "car"]),
        (["cat"] * 2 + ["car"] * 3 + ["cartoon"] * 1, ["car", "cat", "cartoon"]),
    ],
)
def test_sorted_by_use(words, expected):
    trie = CyTrie(words)
    trie.extend(words)
    assert list(trie) == expected
    assert list(trie.complete("ca")) == expected


@pytest.mark.parametrize("words", [["cat"] * 3 + ["car"] * 1 + ["cartoon"] * 2])
def test_query_count(words):
    trie = CyTrie(words)
    trie.extend(words)
    assert trie.count("cat") == 3
    assert trie.count("car") == 1
    assert trie.count("cartoon") == 2
    assert trie.count("carate") == 0
    assert trie.count("ca") == 0


@pytest.mark.parametrize(
    ("input_groups", "expected"),
    [
        (["cv", "as", "rt"], ["car", "cartoon", "carate", "cat"]),
        (["atc", "atc", "atc"], ["cat"]),
        (["c", "a", "r"], ["car", "cartoon", "carate"]),
        (["ct", "a", "tb"], ["cat", "tabla", "table", "taboo"]),
    ],
)
def test_ambiguous_completion(input_groups, expected):
    trie = CyTrie()
    trie.extend(expected)
    assert sorted(trie.complete(input_groups)) == sorted(expected)


@pytest.mark.parametrize(
    ("words", "input_groups", "expected"),
    [(["cat"] * 3 + ["car"], ["cv", "as", "rt"], ["cat", "car"])],
)
def test_ambiguous_completion_sorted_by_use(words, input_groups, expected):
    trie = CyTrie()
    trie.extend(words)
    assert list(trie.complete(input_groups)) == expected