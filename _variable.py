import numpy as np
from collections.abc import Sequence

from ._base import Function, convert
from .exceptions import *

class Variable(Function):

    def __init__(self,
            arg,
            name = None,
            **kwargs,
            ):

        self.nullify()
        self.pipe = None
        self._name = name
        if isinstance(arg, Function):
            self.pipe = arg
            super().__init__(self.pipe, **kwargs)
        elif type(arg) is type:
            if not issubclass(arg, np.generic):
                raise TypeError("dtype must be a Numpy type.")
            dtype = arg
            super().__init__(dtype = dtype, **kwargs)
        elif arg is None:
            super().__init__(None, **kwargs)
        else:
            value = np.array(arg)
            super().__init__(dtype = value.dtype.type, **kwargs)
            self.value = value

    def _isnull(self):
        return self._null
    def nullify(self):
        self._nullify()
    def _nullify(self):
        self._value = None
        self._null = True

    def _evaluate(self):
        if not self.pipe is None:
            self.value = self.pipe
        if self.null:
            raise NullValueDetected
        val = self._value
        if len(val.shape):
            return val
        else:
            return self.dtype(val)

    @property
    def value(self):
        return self.evaluate()
    @value.setter
    def value(self, val):
        if val is None:
            self._value = None
            self._null = True
        else:
            val = self._value_resolve(val)
            self._set_value(val)
            self._null = False
    def _set_value(self, val):
        if self.null:
            self._value = np.array(val, dtype = self.dtype)
        else:
            self._value[...] = val

    def _reassign(self, arg, op = None):
        if self.pipe is None:
            self.value = self._operate(arg, op = op).value
            return self
        else:
            return Variable(self.pipe + arg, **self.kwargs)

    def __iadd__(self, arg): return self._reassign(arg, op = 'add')
    def __ifloordiv__(self, arg): return self._reassign(arg, op = 'floordiv')
    def __imod__(self, arg): return self._reassign(arg, op = 'mod')
    def __imul__(self, arg): return self._reassign(arg, op = 'mul')
    def __ipow__(self, arg): return self._reassign(arg, op = 'pow')
    def __isub__(self, arg): return self._reassign(arg, op = 'sub')
    def __itruediv__(self, arg): return self._reassign(arg, op = 'truediv')

    def pipe_in(self, arg):
        return Variable(convert(arg), **self.kwargs)
    def collect_in(self, arg):
        return Collector(convert(arg), **self.kwargs)

class Collector(Variable, Sequence):

    def _set_value(self, val):
        val = np.array(val, dtype = self.dtype)
        self._values.append(val)
    @property
    def _value(self):
        return np.concatenate(self._values)
    @_value.setter
    def _value(self, val):
        self._values.clear()
        if not val is None:
            self._values.append(self.dtype(val))

    def __len__(self):
        return len(self._values)
    def __iter__(self):
        return iter(self._values)
