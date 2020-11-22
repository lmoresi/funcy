from .._operation import Operation
from ._base import _Seq

class SeqOperation(_Seq, Operation):

    def _iter(self):
        return (self._op_compute(*args) for args in self._iterTerms())

    def _titlestr(self):
        return f'seq[{super()._titlestr()}]'
