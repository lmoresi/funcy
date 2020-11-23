from .._operation import Operation
from ._base import Seq

class IterOp(Seq, Operation):

    def _iter(self):
        return (v for v in self._op_compute(*self._resolve_terms()))

    def _titlestr(self):
        return f'iter[{super()._titlestr()}]'
