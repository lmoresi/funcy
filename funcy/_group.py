from collections.abc import Sequence
from functools import cached_property, lru_cache

from ._derived import Derived

class Group(Derived, Sequence):

    def _operate(self, *args, op = None, **kwargs):
        return Operation(self, *args, op = op, **kwargs)
    def evaluate(self):
        return iter(self)

    def __getitem__(self, arg):
        return self._value_resolve(self.terms[self._value_resolve(arg)])
    def __iter__(self):
        return iter(self.terms)
    def __len__(self):
        return len(self.terms)

from ._operation import Operation
