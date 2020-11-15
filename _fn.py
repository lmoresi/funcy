from .exceptions import *

class _Fn:
    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            cls = Slot
        elif len(args) > 1:
            cls = Seq
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
    def __getitem__(self, arg):
        if isinstance(arg, Sample):
            return arg
        elif type(arg) is tuple:
            return Arbitrary(arg)
        elif type(arg) is slice:
            start, stop, step = arg.start, arg.stop, arg.step
            step = 1 if step is None else step
            if isinstance(step, numbers.Number):
                return Regular(start, stop, step)
            elif isinstance(step, Furcation):
                raise NotYetImplemented
            else:
                if all((
                        isinstance(a, numbers.Integral)
                            for a in (start, stop)
                        )):
                    return Choice(start, stop, step)
                else:
                    return Random(start, stop, step)
        else:
            return Single(arg)

Fn = _Fn()

from ._base import Function
from ._seq import Seq
from ._variable import Variable, MutableVariable
from ._thing import Thing
from ._slot import Slot

from ._sample import *
