from functools import cached_property
import numbers

import reseed

from ..special import *
from .exceptions import *
from ._base import Seq, Seeded

class Discrete(Seq):
    discrete = True
    def _iter(self):
        return iter(self.prime)
    def _seqLength(self):
        return len(self.prime)

class Periodic(Discrete):
    def __init__(self, start, stop, step = None, **kwargs):
        step = 1 if step is None else step
        super().__init__(start, stop, step, **kwargs)
    def _seqLength(self):
        start, stop, step = self._resolve_terms()
        return int((stop - start) / step) + 1
    def _iter(self):
        start, stop, step = self._resolve_terms()
        for i in range(self._seqLength()):
            yield min(start + i * step, stop)

class Random(Seeded, Discrete):
    def __init__(self, low, high, **kwargs):
        super().__init__(low, high, **kwargs)
    def _seqLength(self):
        return len(self._get_iterItems())
    def _iter(self):
        seed = self._startseed
        items = self._get_iterItems()
        while len(items):
            yield items.pop(
                reseed.randint(0, len(items) - 1, seed = seed)
                )
            seed += 1
    def _get_iterItems(self):
        low, high = self._resolve_terms()
        return list(range(low, high + 1))
