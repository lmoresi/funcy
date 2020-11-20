from functools import cached_property
import numbers
from collections.abc import Sequence

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
    def periodic(self):
        from ._discrete import Periodic
        return Periodic
    @cached_property
    def random(self):
        from ._discrete import Random
        return Random
    @cached_property
    def op(self):
        from ..ops import Ops
        from .._constructor import Fn
        from ._seqoperation import SeqOperation
        return Ops(
            Fn.op.rawsource,
            opclass = SeqOperation,
            )
    def __call__(self, arg, **kwargs):
        if isinstance(arg, self.base):
            raise TypeError(arg, type(arg))
        elif type(arg) is slice:
            start, stop, step = arg.start, arg.stop, arg.step
            step = 1 if step is None else step
            if all(isinstance(a, numbers.Integral) for a in (start, stop)):
                if isinstance(step, numbers.Number) or step is None:
                    return self.periodic(start, stop, step, **kwargs)
                else:
                    return self.random(start, stop, step, **kwargs)
            else:
                return self.continuum(start, stop, step, **kwargs)
        elif isinstance(arg, Sequence):
            return self.discrete(arg, **kwargs)
        elif isinstance(arg, Iterable):
            return self.seq(arg, **kwargs)
        else:
            return self.discrete((arg,) **kwargs)
seq = SeqConstructor()
