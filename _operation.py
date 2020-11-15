from functools import cached_property

import operator
import builtins

from ._base import Function
from .exceptions import *

ops = dict(
    getitem = lambda x, y: x[y],
    call = lambda x, y: x(y),
    all = lambda *a: all(a),
    any = lambda *a: any(a),
    )
ops.update({
    'not': lambda x: not x
    })

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
        if len(terms) == 1:
            if isinstance(terms[0], Seq):
                terms = tuple([*terms[0]])
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
        return self.operation(*(
            self._value_resolve(t)
                for t in self.terms
            ))

from ._seq import Seq
