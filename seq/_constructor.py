from functools import cached_property
import numbers
from collections.abc import Sequence, Iterable

class SeqConstructor:
    @cached_property
    def base(self):
        from ._base import _Seq
        return _Seq
    @cached_property
    def seq(self):
        from ._base import Seq
        return Seq
    @cached_property
    def continuum(self):
        from ._continuous import Continuum
        return Continuum
    @cached_property
    def discrete(self):
        from ._discrete import Discrete
        return Discrete
    @cached_property
    def regular(self):
        from ._discrete import Regular
        return Regular
    @cached_property
    def shuffle(self):
        from ._discrete import Shuffle
        return Shuffle
    @cached_property
    def op(self):
        from ..ops import makeops
        from ._seqoperation import SeqOperation
        return makeops(opclass = SeqOperation)
    @cached_property
    def group(self):
        from ._seqgroup import SeqGroup
        return SeqGroup
    @cached_property
    def map(self):
        from ._seqmap import SeqMap
        return SeqMap
    def __call__(self, arg, **kwargs):
        if isinstance(arg, self.base):
            if kwargs:
                raise ValueError("Cannot specify kwargs when type is _Seq.")
            return arg
        elif type(arg) is tuple:
            return self.group(*arg)
        elif type(arg) is slice:
            start, stop, step = arg.start, arg.stop, arg.step
            if isinstance(step, numbers.Number):
                return self.regular(start, stop, step, **kwargs)
            elif any(isinstance(a, numbers.Integral) for a in (start, stop)):
                return self.shuffle(start, stop, step, **kwargs)
            else:
                return self.continuum(start, stop, step, **kwargs)
        elif isinstance(arg, Sequence):
            return self.discrete(arg, **kwargs)
        elif isinstance(arg, Iterable):
            return self.seq(arg, **kwargs)
        else:
            raise TypeError
seq = SeqConstructor()
