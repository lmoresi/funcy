from .._map import Map
from ._base import _Seq
from ._seqgroup import SeqGroup
from .sequtils import seqlength

class SeqMap(_Seq, Map):
    _groupClass = SeqGroup
    def _iter(self):
        return (
            dict(zip(*args))
                for args in self._iterTerms()
            )
    def __getitem__(self, key):
        return (o[key] for o in self)
    def __len__(self):
        return seqlength(self.terms[0])
