from collections.abc import Sequence

from ._base import Function
from .exceptions import *

class Seq(Function, Sequence):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def _evaluate(self):
        return [self._value_resolve(t) for t in self.terms]
    def __getitem__(self, index):
        return self.terms[index]
    def __len__(self):
        return len(self.terms)

    def reduce(self, op = 'call'):
        target = self.terms[0]
        for term in self.terms[1:]:
            target = Fn(target, term).op(op)
        return target
    # def _hashID(self):
    #     return w_hash(tuple(get_hash(t) for t in self.terms))

from ._fn import Fn
