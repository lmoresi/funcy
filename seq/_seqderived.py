from functools import cached_property

from .._derived import Derived
from ..special import *
from ._base import Seq
from .sequtils import seqlength


class SeqDerived(Seq, Derived):
    @cached_property
    def seqTerms(self):
        return [t for t in self.fnTerms if isinstance(t, Seq)]
    def _seqLength(self):
        if self.seqTerms:
            v = 1
            for t in self.seqTerms:
                v *= seqlength(t)
            return v
        else:
            return unkint
