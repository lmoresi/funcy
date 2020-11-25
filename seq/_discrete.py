from functools import cached_property
import numbers

import reseed

from ..special import *
from ._base import Seq, Seeded
from ._seqderived import SeqDerived
from .exceptions import *

class Discrete(SeqDerived):
    discrete = True
    def _iter(self):
        return iter(self.prime)
    def _seqLength(self):
        return len(self.prime)

class Regular(Discrete):
    def __init__(self, start = 0, stop = 1, step = 1, **kwargs):
        start = 0 if start is None else start
        stop = 1 if stop is None else stop
        step = 1 if step is None else step
        super().__init__(start, stop, step, **kwargs)
    def _iter(self):
        start, stop, step = self._resolve_terms()
        for i in range(self._seqLength()):
            yield min(start + i * step, stop)
    def _seqLength(self):
        start, stop, step = self._resolve_terms()
        return int((stop - start) / step) + 1

class Shuffle(Seeded, Discrete):
    def __init__(self, start = 0, stop = 1, seed = None, **kwargs):
        start = 0 if start is None else start
        stop = 1 if stop is None else stop
        super().__init__(start, stop, seed, **kwargs)
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
        start, stop, _ = self._resolve_terms()
        return list(range(start, stop))
