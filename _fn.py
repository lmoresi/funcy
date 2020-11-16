from .exceptions import *

class _Fn:
    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            cls = Slot
        elif len(args) > 1:
            return Group(*args, **kwargs)
        else:
            arg = args[0]
            if len(kwargs) == 0 and isinstance(arg, Function):
                return arg
            check = Variable._check_arg(arg)
            if check is None:
                cls = Thing
            else:
                cls = MutableVariable
        return cls(*args, **kwargs)
    def __getitem__(self, arg, **kwargs):
        if isinstance(arg, Seq):
            raise TypeError(arg, type(arg))
        elif type(arg) is tuple:
            return Seq(arg, **kwargs)
        elif type(arg) is slice:
            start, stop, step = arg.start, arg.stop, arg.step
            step = 1 if step is None else step
            if isinstance(step, Furcation):
                raise NotYetImplemented
            try:
                return PeriodicSeq(start, stop, step, **kwargs)
            except FunctionCreationException:
                try:
                    return Continuum(start, stop, step, **kwargs)
                except FunctionCreationException:
                    return RandomSeq(start, stop, step, **kwargs)
        else:
            return Seq((arg,) **kwargs)

Fn = _Fn()

from ._base import Function
from ._variable import Variable, MutableVariable
from ._group import Group
from ._thing import Thing
from ._slot import Slot

from ._seq import *
