from collections.abc import Sequence
from functools import cached_property, lru_cache

from ._base import Function

class Group(Function, Sequence):

    def _operate(self, *args, op = None, truthy = False, **kwargs):
        return Operation(self, *args, op = op, **kwargs)
    def evaluate(self):
        return iter(self)

    @lru_cache(32)
    def __getitem__(self, arg):
        try:
            return self.terms[arg]
        except TypeError:
            try:
                return self.terms[self.keysDict[arg]]
            except AttributeError:
                raise IndexError
    def __iter__(self):
        return iter(self.terms)
    def __len__(self):
        return self._length
    @cached_property
    def _length(self):
        return len(self.terms)

from ._operation import Operation
