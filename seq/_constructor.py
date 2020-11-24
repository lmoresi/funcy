from functools import cached_property
import numbers
from collections.abc import Sequence, Iterable

from .samplers import Sampler

class SeqConstructor:
    @cached_property
    def base(self):
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
                raise ValueError("Cannot specify kwargs when type is Seq.")
            return arg
        elif type(arg) is tuple:
            return self.group(*arg)
        elif type(arg) is slice:
            start, stop, step = arg.start, arg.stop, arg.step
            if isinstance(step, numbers.Number):
                return self.regular(start, stop, step, **kwargs)
            elif type(step) is str or step is None:
                if any(isinstance(a, numbers.Integral) for a in (start, stop)):
                    return self.shuffle(start, stop, step, **kwargs)
                else:
                    return self.continuum(start, stop, step, **kwargs)
            elif isinstance(step, Sampler):
                return step(start, stop)
            else:
                raise TypeError(
                    "Could not understand 'step' input of type:", type(step)
                    )
        elif isinstance(arg, Sequence):
            return self.discrete(arg, **kwargs)
        else:
            return self.base(arg, **kwargs)
    def __getattr__(self, key):
        return getattr(self.op, key)
seq = SeqConstructor()
