from functools import cached_property, lru_cache
from itertools import product
import operator
import builtins

from ._base import Function
from .exceptions import *

ops = dict(
    getitem = lambda x, y: x[y],
    call = lambda x, y: x(y),
    all = lambda a: all(a),
    any = lambda a: any(a),
    inv = lambda a: not a,
    )

def getop(op):
    if op is None:
        return lambda *args: args
    elif type(op) is str:
        if op in ops:
            return ops[op]
        else:
            try:
                return getattr(builtins, op)
            except AttributeError:
                return getattr(operator, op)
    else:
        assert callable(op)
        return op

class Operation(Function):
    def __init__(self,
            *terms,
            op = None,
            ):
        if type(op) is tuple:
            sops, op = op[:-1], op[-1]
            for sop in sops:
                terms = Operation(*terms, op = sop)
                if not type(terms) is tuple:
                    terms = terms,
        super().__init__(*terms, op = op)
    @cached_property
    def operation(self):
        return getop(self.kwargs['op'])
    def _evaluate(self):
        if self.isiter:
            return SeqIterable(self)
        else:
            return self._op_compute(*self.terms)
    def _op_compute(self, *args):
        try:
            return self.operation(*(
                self._value_resolve(a)
                    for a in args
                ))
        except Exception as e:
            print(args)
            raise e
    def _iter(self):
        return (self._op_compute(*args) for args in self._iterProd())
    def _iterProd(self):
        return product(*self._termsAsIters)
    @cached_property
    def _seqLength(self):
        v = 1
        for t in self.iterTerms:
            v *= len(t.value)
        return v

class Reduction(Operation):
    pass

# At bottom to avoid circular reference (should fix this):
from ._seq import SeqIterable
