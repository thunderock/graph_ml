import numpy as np
from scipy import sparse
from numba import njit

def to_member_matrix(group_ids):
    """
    create a member matrix U such that U[i,k] = 1 if i belongs to group k otherwise U[i,k]=0
    :param group_ids:
    :return:
    """
    Nr = group_ids.shape[0] # equal to number of samples
    Nc = int(np.max(group_ids) + 1) # number of classes
    U = sparse.csr_matrix((np.ones_like(group_ids), (np.arange(Nr), group_ids)), shape=(Nr, Nc))
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



