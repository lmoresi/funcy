import numpy as np
from collections.abc import Sequence

from ._base import Function, convert
from .exceptions import *



class Variable(Function):

    @staticmethod
    def _check_arg(arg):
        if isinstance(arg, Function):
            return 'pipe'
        elif type(arg) is type:
            return 'dtype'
        elif arg is None:
            return 'empty'
        else:
            if np.array(arg).dtype == 'O':
                return None
            else:
                return 'numeric'

    def __init__(self,
            arg,
            name = None,
            **kwargs,
            ):

        self.nullify()
        self.pipe = None
        self._name = name
        check = self._check_arg(arg)
        if check == 'pipe':
            self.pipe = arg
            super().__init__(self.pipe, **kwargs)
        elif check == 'dtype':
            super().__init__(dtype = arg, **kwargs)
        elif check == 'empty':
            super().__init__(None, **kwargs)
        elif check == 'numeric':
            if not isinstance(arg, np.ndarray):
                arg = np.array(arg)
            super().__init__(dtype = arg.dtype.type, **kwargs)
            self._value = arg
            self.value = arg
        else:
            raise ValueError(arg)

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
        raise MissingAsset

    def _reassign(self, arg, op = None):
        if self.pipe is None:
            self.value = self._operate(arg, op = op).value
            return self
        else:
            return Variable(self.pipe + arg, **self.kwargs)

class FixedVariable(Variable):

    def _set_value(self, val):
        try:
            self._value[...] = val
        except TypeError:
            self._value = np.array(val, dtype = self.dtype)

class ExtendableVariable(Variable, Sequence):

    def _set_value(self, val):
        val = np.array(val, dtype = self.dtype)
        self.values.append(val)
    @property
    def _value(self):
        return np.stack(self._values)
    @_value.setter
    def _value(self, val):
        self.values.clear()
        if not val is None:
            self.values.append(self.dtype(val))
    @property
    def values(self):
        try:
            return self._values
        except AttributeError:
            self._values = []
            return self._values

    def __len__(self):
        return len(self.values)
    def __iter__(self):
        return iter(self.values)
