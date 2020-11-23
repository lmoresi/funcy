from .._group import Group
from ._base import Seq
from .sequtils import seqlength

class SeqGroup(Seq, Group):

    def _iter(self):
        return self._iterTerms()
