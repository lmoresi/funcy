from functools import wraps

import numpy as np
from collections.abc import Sequence

from ._base import Function, getop
from .exceptions import *

def nullwrap(func):
    @wraps(func)
    def wrapper(self, arg, **kwargs):
        # if arg is None:
        #     raise NullValueDetected
        try:
            return func(self, arg, **kwargs)
        except TypeError:
            if self.null:
                raise NullValueDetected
            else:
                return func(self, self._value_resolve(arg))
    return wrapper

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

    __slots__ = (
        '_value_resolve',
        'data',
        'pipe',
        'dtype',
        '_name',
        'scalar',
        'terms',
        'arg',
        'kwargs',
        'isnull',
        '_set_value',
        )

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
            raise NotYetImplemented
            # self.pipe = arg
            # super().__init__(self.pipe, name = name, **kwargs)
        elif check == 'dtype':
            self.dtype = arg
            self.scalar = True
            super().__init__(name = name, **kwargs)
        elif check == 'empty':
            super().__init__(Function(), name = name, **kwargs)
        elif check == 'numeric':
            if isinstance(arg, np.ndarray):
                asarr = arg
                self.scalar = False
            else:
                asarr = np.array(arg)
                self.scalar = True
            self.dtype = asarr.dtype.type
            super().__init__(name = name, **kwargs)
        else:
            raise ValueError(arg)
        if self.scalar:
            self.isnull = lambda: self.data is None
            self._set_value = self._set_value_scalar
        else:
            self.isnull = lambda: np.isnull(self.data).any()
            self._set_value = self._set_value_array
        if check == 'numeric':
            self.value = arg

    def nullify(self):
        self._nullify()
    def _nullify(self):
        self.data = None
    @property
    def null(self):
        return self.isnull()

    def _evaluate(self):
        return self.value
    def out(self):
        if self.scalar:
            return self.data
        else:
            return self.data.copy()

    @property
    def value(self):
        data = self.data
        if data is None: raise NullValueDetected
        return data
    @value.setter
    def value(self, val):
        self._set_value(val)
        # if self.pipe is None:
        #     if val is None:
        #         self.data = None
        #         self.null = True
        #     else:
        #         self._set_value(val)
        #         self.null = False
        # else:
        #     raise NotYetImplemented
    # def _reassign(self, arg, op = None):
    #     if self.pipe is None:
    #         self._set_value(getop(op)(self.data, self._value_resolve(arg)))
    #         return self
    #     else:
    #         return Variable(self.pipe + arg, **self.kwargs)

class MutableVariable(Variable):

    def _set_value_scalar(self, val):
        try:
            self.data = self.dtype(self._value_resolve(val))
        except TypeError:
            self.data = None
    def _set_value_array(self, val):
        try:
            self.data[...] = self._value_resolve(val)
        except TypeError:
            self.data = np.array(
                self._value_resolve(val),
                dtype = self.dtype
                )

    @nullwrap
    def __iadd__(self, arg):
        self.data += arg
        return self
    @nullwrap
    def __isub__(self, arg):
        self.data -= arg
        return self
    @nullwrap
    def __imul__(self, arg):
        self.data *= arg
        return self
    @nullwrap
    def __itruediv__(self, arg):
        self.data /= arg
        return self
    @nullwrap
    def __ifloordiv__(self, arg):
        self.data //= arg
        return self
    @nullwrap
    def __imod__(self, arg):
        self.data %= arg
        return self
    @nullwrap
    def __ipow__(self, arg):
        self.data **= arg
        return self

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
