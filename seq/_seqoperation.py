from .._operation import Operation, Operations
from ._seqderived import SeqDerived
from ._base import Seq

class SeqOperation(SeqDerived, Operation):

    def _iter(self):
        return (v for v in self._op_compute(*self._resolve_terms()))

    def _titlestr(self):
        return f'seq[{super()._titlestr()}]'

class SeqOperations(Operations):
    pass
