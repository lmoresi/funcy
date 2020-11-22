import numpy as np

from diversipy import hycusampling

from . import reseed

@reseed.reseed
def latin_hypercube(n, d, lower = 0, upper = 1):
    from diversipy.hycusampling import improved_lhd_matrix
    lower, upper = (
        np.full(d, bnd) if not isinstance(bnd, np.ndarray)
            else bnd for bnd in (lower, upper)
        )
    samples = improved_lhd_matrix(n, d)
    return samples / n * (upper - lower) + lower
