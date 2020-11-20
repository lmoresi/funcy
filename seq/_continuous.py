import reseed

from ..utilities import process_scalar
from ..special import *
from ._base import _Seq, Seeded

class Continuous(_Seq):
    def _seqLength(self):
        return inf

class Continuum(Continuous, Seeded):
    def __init__(self, start, stop, step = None, **kwargs):
        super().__init__(start, stop, step, **kwargs)
    def _iter(self):
        start, stop, _ = self._resolve_terms()
        seed = self._startseed
        while True:
            v = reseed.rangearr(start, stop, seed = seed)
            if not len(v.shape):
                v = process_scalar(v)
            yield v
            seed += 1