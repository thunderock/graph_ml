# distutils: language = c++

from libcpp.list cimport list
from libcpp.string cimport string


cdef extern from "Trie.cpp":
    pass

cdef extern from "Trie.h":
    cdef cppclass Trie:
        Trie() except +
        void insert(string, int)
        int count(string) const
        list[string] complete(const string) const
        list[string] ambiguous_complete(const list[string]) const
        void extend(const list[string] words, list[int] multipliers)
