import itertools
from collections import OrderedDict

from .._map import Map
from ._base import Seq
from ._seqderived import SeqDerived
from ._seqgroup import SeqGroup
from .sequtils import seqlength

class SeqMap(SeqDerived, Map):
    _groupClass = SeqGroup
    def _iter(self):
        for ks, vs in self._iterTerms():
            iterDict = OrderedDict(self._unpack_tuple(ks, vs))
            valGroup = SeqGroup(*iterDict.values())
            for valset in valGroup._iterTerms():
                yield dict(zip(iterDict.keys(), valset))

    def _unpack_tuple(self, ks, vs):
        for k, v in zip(ks, vs):
            if type(k) is tuple:
                for sk, sv in self._unpack_tuple(k, v):
                    yield sk, sv
            else:
                yield k, v
    def __getitem__(self, key):
        return (o[key] for o in self)
    def __len__(self):
        return seqlength(self.terms[0])
