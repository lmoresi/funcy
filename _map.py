from collections.abc import Mapping

from ._derived import Derived
from ._group import Group

class Map(Derived, Mapping):
    _groupClass = Group
    @classmethod
    def kw(cls, **kwargs):
        return cls(kwargs.keys(), kwargs.values())
    def __init__(self,
            *args,
            pairwise = True,
            **kwargs,
            ):
        if pairwise:
            keys, values = zip(*args)
        else:
            keys, values = self._groupClass(*keys), self._groupClass(*values)
        if pairwise:
            super().__init__(keys, values, **kwargs)
        else:
            super().__init__(keys, values, pairwise = False, **kwargs)
    def evaluate(self):
        return dict(zip(*self._resolve_terms()))
    def __getitem__(self, key):
        return self.value[self._value_resolve(key)]
    def __len__(self):
        return len(self.terms[0])
    def __iter__(self):
        return self.terms[0]._resolve_terms()
