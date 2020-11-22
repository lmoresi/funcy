from collections.abc import Mapping

from ._base import Function
from ._group import Group

class Map(Function, Mapping):
    _groupClass = Group
    def __init__(self,
            keys,
            values,
            **kwargs,
            ):
        keys, values = self._groupClass(*keys), self._groupClass(*values)
        super().__init__(keys, values, **kwargs)
    def evaluate(self):
        return dict(zip(*self._resolve_terms()))
    def __getitem__(self, key):
        return self.value[self._value_resolve(key)]
    def __len__(self):
        return len(self.terms[0])
    def __iter__(self):
        return self.terms[0]._resolve_terms()
