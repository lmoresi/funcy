from functools import cached_property, lru_cache
from itertools import product

from ._base import Function
from . import utilities

class Operation(Function):
    __slots__ = ('opkwargs', 'opfn')

    def __init__(self,
            *terms,
            op = None,
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
        super().__init__(*terms, op = op, **kwargs)

    def _evaluate(self):
        return self._op_compute(*self.terms)
    def _op_compute(self, *args):
        return self.opfn(
            *(self._value_resolve(a) for a in args),
            **self.opkwargs,
            )

    def _titlestr(self):
        return self.opfn.__name__
    def _kwargstr(self):
        kwargs = self.opkwargs.copy()
        if kwargs:
            return utilities.kwargstr(**kwargs)
        else:
            return ''
