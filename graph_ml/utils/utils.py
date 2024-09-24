import os

import numpy as np
from numba import njit
from scipy import sparse


def get_formatted_environ_variable(name, dtype, default):
    """
    get the environment variable with name `name` and convert it to `dtype`
    if it is not available return the default value
    :param name:
    :param dtype:
    :param default:
    :return:
    """
    value = os.environ.get(name)
    if value is None:
        return default
    if dtype == bool:
        return value.lower() not in ["0", "false", "False", "FALSE"]
    return dtype(value)


def to_member_matrix(group_ids):
    """
    create a member matrix U such that U[i,k] = 1 if i belongs to group k else U[i,k]=0
    :param group_ids:
    :return:
    """
    Nr = group_ids.shape[0]  # equal to number of samples
    Nc = int(np.max(group_ids) + 1)  # number of classes
    U = sparse.csr_matrix(
        (np.ones_like(group_ids), (np.arange(Nr), group_ids)), shape=(Nr, Nc)
    )
    U.data = U.data * 0 + 1
    return U


def matrix_sum_power(A, T):
    """
    compute the sum of the powers of the matrix A i.e.,
    sum_{t=1}^{T} A^t
    :param A:
    :param T:
    :return:
    """
    At = np.eye(A.shape[0])
    As = np.zeros((A.shape[0], A.shape[0]))
    for _ in range(T):
        At = A @ At
        As += At
    return As


@njit(nogil=True)
def csr_row_cumsum(indptr, data):
    """
    compute the cumulative sum of the data array using the indptr array
    :param indptr:
    :param data:
    :return:
    """
    out = np.zeros_like(data)
    for i in range(len(indptr) - 1):
        start = indptr[i]
        end = indptr[i + 1]
        out[start:end] = np.cumsum(data[start:end])
    return out


def sample_csr(rows, csr_mat):
    return _sample_csr(rows, csr_mat.indptr, csr_mat.indices, csr_mat.data)


@njit(nogil=True)
def _neighbors(indptr, indices_or_data, t):
    return indices_or_data[indptr[t] : indptr[t + 1]]


@njit(nogil=True)
def _sample_csr(rows, indptr, indices, data):
    n = len(rows)
    retval = np.empty(n, dtype=indices.dtype)
    for j in range(n):
        neighbors = _neighbors(indptr, indices, rows[j])
        neighbors_p = _neighbors(indptr, data, rows[j])
        retval[j] = neighbors[np.searchsorted(neighbors_p, np.random.rand())]
    return retval
