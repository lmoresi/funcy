from ._base import Seq
from ..variable import Scalar
from ..special import *

class Algorithmic(Seq):
    __slots__ = ('n', 'algorithm',)
    def __init__(self, algorithm, **kwargs):
        self.n = Scalar(0, name = 'n')
        self.algorithm = algorithm.close(_seq_n = self.n)
        super().__init__(algorithm, **kwargs)
    def _iter(self):
        self.n.set(-1)
        while True:
            self.n += 1
            yield self.algorithm.value
    def _seqLength(self):
        return inf
