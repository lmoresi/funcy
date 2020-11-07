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
            asList = False,
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
        self.operation = getop(op)
        self.asList = asList
        super().__init__(*terms, op = op)

    def _evaluate(self):
        try:
            ts = [self._value_resolve(t) for t in self.terms]
            if self.asList:
                out = self.operation(ts)
            else:
                out = self.operation(*ts)
            return out
        except NullValueDetected:
            raise NullValueDetected

from ._seq import Seq
