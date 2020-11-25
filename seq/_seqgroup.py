from .._group import Group
from ._base import Seq
from ._seqderived import SeqDerived
from .sequtils import seqlength

class SeqGroup(SeqDerived, Group):

    def _iter(self):
        return self._iterTerms()
