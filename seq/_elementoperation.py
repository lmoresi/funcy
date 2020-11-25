from .._operation import Operation, Operations
from ._base import Seq
from ._seqderived import SeqDerived
from .exceptions import *

class ElementOp(SeqDerived, Operation):

    def _iter(self):
        return (self._op_compute(*args) for args in self._iterTerms())

    def _titlestr(self):
        return f'[{super()._titlestr()}]'

class ElementOps(Operations):
    pass
