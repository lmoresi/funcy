from .._group import Group
from ._base import _Seq
from .sequtils import seqlength

class SeqGroup(_Seq, Group):

    def _iter(self):
        return self._iterTerms()
