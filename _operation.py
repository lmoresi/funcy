from functools import cached_property, lru_cache
from itertools import product
import operator
import builtins
import itertools

import numpy as np
import scipy as sp

from ._base import Function
from . import utilities
from .exceptions import *

class Operation(Function):
    __slots__ = ('opkwargs', 'opkey', 'opfn')
    def __init__(self,
            *terms,
            op = None,
            seq = True,
            **kwargs,
            ):
        if type(op) is tuple:
            sops, op = op[:-1], op[-1]
            for sop in sops:
                terms = Operation(*terms, op = sop)
                if not type(terms) is tuple:
                    terms = terms,
        self.opkwargs = kwargs
        self.opfn = op
        super().__init__(*terms, op = op, seq = seq, **kwargs)
    @cached_property
    def seqIterable(self):
        return SeqIterable(self)
    @cached_property
    def _op_method(self):
        if self.opseq: return lambda: self.seqIterable
        else: return lambda: self._op_compute(*self.terms)
    @cached_property
    def opseq(self):
        if self.kwargs['seq']:
            if self.isSeq:
                return True
        return False
    def _evaluate(self):
        return self._op_method()
    def _op_compute(self, *args):
        return self.opfn(
            *(self._value_resolve(a) for a in args),
            **self.opkwargs,
            )
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
    def _titlestr(self):
        return self.opfn.__name__

    def _kwargstr(self):
        kwargs = self.opkwargs.copy()
        if self.isSeq and not self.opseq:
            kwargs['seq'] = False
        if kwargs:
            return utilities.kwargstr(**kwargs)
        else:
            return ''

# At bottom to avoid circular reference (should fix this):
from .seq import SeqIterable, seqlength
