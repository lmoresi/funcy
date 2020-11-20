from functools import cached_property, lru_cache
import itertools

from .._operation import Operation
from ._base import _Seq

class SeqOperation(Operation, _Seq):

    def _iter(self):
        return (self._op_compute(*args) for args in self._iterProd())
    def _iterProd(self):
        return product(*(
            t.value if t in self.seqTerms else (t,)
                for t in self.terms
            ))

    def _seqLength(self):
        v = 1
        for t in self.seqTerms:
            v *= seqlength(t)
        return v
    @cached_property
    def seqTerms(self):
        return [t for t in self.fnTerms if isinstance(t, _Seq)]

    def _titlestr(self):
        return f'seq[{super()._titlestr()}]'
