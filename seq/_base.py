from functools import cached_property
from collections.abc import Iterable
from itertools import product

import reseed

from .._base import Function
from ..special import *
from ._seqiterable import SeqIterable
from .sequtils import seqlength
from .exceptions import *

class _Seq(Function, Iterable):

    discrete = False

    def __iter__(self):
        return iter(self.seqIterable)
    def _iterTerms(self):
        return product(*(
            (t,) if not isinstance(t, Iterable) else t
                for t in self._resolve_terms()
            ))
    @cached_property
    def seqIterable(self):
        return SeqIterable(self)

    def evaluate(self):
        return self.seqIterable
    def refresh(self):
        super().refresh()
        self.seqIterable._get_index.cache_clear()
        self.seqIterable._get_slice.cache_clear()

    def _iter(self):
        raise MissingAsset

    def _seqLength(self):
        if self.seqTerms:
            v = 1
            for t in self.seqTerms:
                v *= seqlength(t)
            return v
        else:
            return inf
    @cached_property
    def seqTerms(self):
        return [t for t in self.fnTerms if isinstance(t, _Seq)]

    @cached_property
    def _opman(self):
        from ._constructor import seq
        return seq.op

class Seq(_Seq):
    def __init__(self, iterable, **kwargs):
        super().__init__(iterable, **kwargs)
    def _iter(self):
        return iter(self._value_resolve(self.prime))

class UnSeq(Function):
    def __init__(self, seq):
        if not seq.isSeq:
            raise TypeError("Cannot unseq non-seq.")
        super().__init__(seq)
    def evaluate(self):
        return self.prime.value
    def seqTerms(self):
        return []
    @property
    def isSeq(self):
        return False

class Seeded(_Seq):
    @cached_property
    def _startseed(self):
        return reseed.digits(12, self.terms[2])

from ._constructor import seq
