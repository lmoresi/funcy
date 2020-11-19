from functools import cached_property
import numbers

import reseed

from .._base import Function
from .. import utilities
from ..utilities import process_scalar
from ..special import *
from ._seqiterable import SeqIterable
from .exceptions import *

class Seq(Function):
    discrete = False
    isSeq = True
    @cached_property
    def seqIterable(self):
        return SeqIterable(self)
    def _evaluate(self):
        return self.seqIterable
    def refresh(self):
        super().refresh()
        self.seqIterable._get_index.cache_clear()
        self.seqIterable._get_slice.cache_clear()
    def _iter(self):
        raise MissingAsset
    def _seqLength(self):
        raise MissingAsset

class UnSeq(Function):
    def __init__(self, seq):
        if not seq.isSeq:
            raise TypeError("Cannot unseq non-seq.")
        super().__init__(seq)
    def _evaluate(self):
        return self.prime.value
    def seqTerms(self):
        return []
    @property
    def isSeq(self):
        return False

class Seeded(Seq):
    @cached_property
    def _startseed(self):
        return reseed.digits(12, self.terms[2])

class Continuum(Seq):
    def __init__(self, start, stop, step = None, **kwargs):
        super().__init__(start, stop, step, **kwargs)
    def _seqLength(self):
        return inf
    def _iter(self):
        start, stop, _ = self._resolve_terms()
        seed = self._startseed
        while True:
            v = reseed.rangearr(start, stop, seed = seed)
            if not len(v.shape):
                v = process_scalar(v)
            yield v
            seed += 1
