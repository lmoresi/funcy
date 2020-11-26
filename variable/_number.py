from functools import wraps

from ._base import Variable
from .exceptions import *

class Number(Variable):

    __slots__ = (
        'dtype',
        )

    def __init__(self, dtype, *args, **kwargs,):
        self.dtype = dtype
        super().__init__(dtype, *args, **kwargs,)

    def nullify(self):
        raise MissingAsset
    @property
    def isnull(self):
        raise MissingAsset

    def __iadd__(self, arg):
        try:
            self.data += arg
        except TypeError:
            self.data += self._value_resolve(arg)
        self.refresh()
        return self
    def __isub__(self, arg):
        try:
            self.data -= arg
        except TypeError:
            self.data -= self._value_resolve(arg)
        self.refresh()
        return self
    def __imul__(self, arg):
        try:
            self.data *= arg
        except TypeError:
            self.data *= self._value_resolve(arg)
        self.refresh()
        return self
    def __itruediv__(self, arg):
        try:
            self.data /= arg
        except TypeError:
            self.data /= self._value_resolve(arg)
        self.refresh()
        return self
    def __ifloordiv__(self, arg):
        try:
            self.data //= arg
        except TypeError:
            self.data //= self._value_resolve(arg)
        self.refresh()
        return self
    def __imod__(self, arg):
        try:
            self.data %= arg
        except TypeError:
            self.data %= self._value_resolve(arg)
        self.refresh()
        return self
    def __ipow__(self, arg):
        try:
            self.data **= arg
        except TypeError:
            self.data **= self._value_resolve(arg)
        self.refresh()
        return self

# To those wondering,
# the code here is repetitive deliberately
# due to unavoidable performance issues
# when invoking more sophisticated Python syntax.
# Ultimately, the whole thing should be rewritten
# in Cython.
# Performance is currently within an order of magnitude
# of a 'pure' Python approach.
