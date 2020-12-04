from collections.abc import Mapping
from collections import OrderedDict

from ..utilities import unpack_tuple
from ._derived import Derived

class Map(Derived, Mapping):
    def __init__(self,
            keys,
            values,
            **kwargs,
            ):
        super().__init__(keys, values, **kwargs)
    def evaluate(self):
        return OrderedDict(unpack_tuple(*self._resolve_terms()))
    def __getitem__(self, key):
        return self.value[self._value_resolve(key)]
    def __len__(self):
        return len(self.terms[0])
    def __iter__(self):
        return self.terms[0]._resolve_terms()
