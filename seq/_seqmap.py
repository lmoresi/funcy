from collections import OrderedDict

from .._map import Map
from ._base import Seq
from .sequtils import seqlength
from .seqoperations import muddle

class SeqMap(Seq, Map):
    _groupClass = SeqGroup
    def _iter(self):
        for ks, vs in muddle(self.terms):
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
    def __len__(self):
        return seqlength(self.terms[0])
