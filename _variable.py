import numpy as np
from collections.abc import Sequence

from ._base import Function
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
        self.dtype = None
        self._name = name
        check = self._check_arg(arg)
        if check == 'pipe':
            self.pipe = arg
            super().__init__(self.pipe, name = name, **kwargs)
        elif check == 'dtype':
            self.dtype = arg
            super().__init__(name = name, **kwargs)
        elif check == 'empty':
            super().__init__(Function(), name = name, **kwargs)
        elif check == 'numeric':
            if not isinstance(arg, np.ndarray):
                arg = np.array(arg)
            self.dtype = arg.dtype.type
            super().__init__(name = name, **kwargs)
            self.data = arg
            self.value = arg
        else:
            raise ValueError(arg)

    def _isnull(self):
        return self._null
    def nullify(self):
        self._nullify()
    def _nullify(self):
        self.data = None
        self._null = True

    def _evaluate(self):
        if not self.pipe is None:
            self.value = self.pipe
        if self.null:
            raise NullValueDetected
        val = self.data
        if len(val.shape):
            return val
        else:
            if not self.dtype is None:
                val = self.dtype(val)
            return val

    @property
    def value(self):
        return self.evaluate()
    @value.setter
    def value(self, val):
        if val is None:
            self.data = None
            self._null = True
        else:
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
        val = self._value_resolve(val)
        try:
            self.data[...] = val
        except TypeError:
            self.data = np.array(val, dtype = self.dtype)

class ExtendableVariable(Variable, Sequence):

    def _set_value(self, val):
        val = self._value_resolve(val)
        val = np.array(val, dtype = self.dtype)
        self.values.append(val)
    @property
    def data(self):
        return np.stack(self.datas)
    @data.setter
    def data(self, val):
        self.values.clear()
        if not val is None:
            self.values.append(self.dtype(val))
    @property
    def values(self):
        try:
            return self.datas
        except AttributeError:
            self.datas = []
            return self.datas

    def __len__(self):
        return len(self.values)
    def __iter__(self):
        return iter(self.values)
