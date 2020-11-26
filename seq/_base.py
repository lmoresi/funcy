from functools import cached_property
from collections.abc import Iterable
from itertools import product

import reseed

from .. import Fn
from .._base import Function
from .._derived import Derived
from ..special import *
from ._seqiterable import SeqIterable
from .sequtils import seqlength
from .exceptions import *

class Seq(Derived, Iterable):

    discrete = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def seqIterable(self):
        return SeqIterable(self)

    def evaluate(self):
        return self.seqIterable
    def update(self):
        super().update()
        self.seqIterable._get_index.cache_clear()
        self.seqIterable._get_slice.cache_clear()

    def _iter(self):
        return iter(self._value_resolve(self.prime))

    def __iter__(self):
        return iter(self.value)

    @cached_property
    def seqTerms(self):
        return [t for t in self.fnTerms if isinstance(t, Seq)]
    def _seqLength(self):
        return unkint
    def __len__(self):
        return self._seqLength()

    def op(self, *args, op, rev = False, **kwargs):
        return Fn[
            Fn.op.starmap(
                Fn.op.getfn(op),
                Fn[(*args, self) if rev else (self, *args)],
                )
            ]

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

class Seeded(Seq):
    @cached_property
    def _startseed(self):
        return reseed.digits(12, seed = self._value_resolve(self.terms[-1]))

    # def __len__(self):
    #     return len(self.value[0])
    # def __getitem__(self, arg):
    #     if type(arg) is slice:
    #         return self._getslice(arg)
    #     else:
    #         return self.op(arg, op = 'getitem')
    # def _getslice(self, slicer):
    #     start, stop, step = slicer.start, slicer.stop, slicer.step
    #     start = 0 if start is None else start
    #     stop = len(self) if stop is None else min(len(self, stop))
    #     step = 1 if step is None else step
    #     return (self[i] for i in range(start, stop, step))
    # def __iter__(self):
    #     return (self[i] for i in range(len(self)))

from ._constructor import seq
