import numpy as np
from collections.abc import Sequence
from functools import cached_property, lru_cache

from .exceptions import *

from ._base import Function, refresh_wrap
from .special import null


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

        self.data = null
        self.pipe = None
        self.dtype = None
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
            super().__init__(Fn(), name = name, **kwargs)
        elif check == 'numeric':
            if isinstance(arg, (np.ndarray, Sequence)):
                asarr = np.array(arg)
                self.scalar = False
                self._length = len(asarr)
            else:
                asarr = np.array(arg)
                self.scalar = True
            self.dtype = asarr.dtype.type
            super().__init__(name = name, **kwargs)
        else:
            raise ValueError(arg)
        if self.scalar:
            self._set_value = self._set_value_scalar
        else:
            self._set_value = self._set_value_array
        if check == 'numeric':
            self.value = arg

    def nullify(self):
        self.value = None
    @property
    def null(self):
        try:
            self.data + 0
            return False
        except NullValueDetected:
            return True

    def evaluate(self):
        return self.data
    def out(self):
        if self.scalar:
            return self.data
        else:
            return self.data.copy()

    @property
    def value(self):
        return self.evaluate()
        # return self.data
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

    # @cached_property
    # def _set_value(self):
    #     if self.scalar: return self._set_value_scalar
    #     else: return self._set_value_array
    @refresh_wrap
    def _set_value_scalar(self, val):
        try:
            self.data = self.dtype(self._value_resolve(val))
        except (NullValueDetected, TypeError):
            self.data = null
    @refresh_wrap
    def _set_value_array(self, val):
        val = null if val is None else val
        try:
            self.data[...] = self._value_resolve(val)
        except NullValueDetected:
            try:
                val = self._value_resolve(val)
                self.data = np.array(
                    self._value_resolve(val)
                    ).astype(self.dtype)
            except (NullValueDetected, TypeError):
                self.data = null

    def __iadd__(self, arg):
        self.value = arg + self.data
        return self
    def __isub__(self, arg):
        self.value -= arg
        return self
    def __imul__(self, arg):
        self.value *= arg
        return self
    def __itruediv__(self, arg):
        self.value /= arg
    def __ifloordiv__(self, arg):
        self.value //= arg
        return self
    def __imod__(self, arg):
        self.value %= arg
        return self
    def __ipow__(self, arg):
        self.value **= arg
        return self

# class ExtendableVariable(Variable, Sequence):
#
#     def _set_value(self, val):
#         val = self._value_resolve(val)
#         val = np.array(val, dtype = self.dtype)
#         self.values.append(val)
#     @property
#     def data(self):
#         return np.stack(self.datas)
#     @data.setter
#     def data(self, val):
#         self.values.clear()
#         if not val is None:
#             self.values.append(self.dtype(val))
#     @property
#     def values(self):
#         try:
#             return self.datas
#         except AttributeError:
#             self.datas = []
#             return self.datas
#
#     def __len__(self):
#         return len(self.values)
#     def __iter__(self):
#         return iter(self.values)

# At bottom to avoid circular reference:
from ._constructor import Fn
