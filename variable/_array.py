import numpy as np
from collections.abc import Sequence

from ._number import Number
from .exceptions import *

class Array(Number):

    __slots__ = (
        '_isnull',
        )

    def __init__(self,
            arg1,
            arg2 = None,
            /,
            *args,
            **kwargs
            ):
        if arg2 is None:
            if isinstance(arg1, Sequence):
                arg1 = np.array(arg1)
            if isinstance(arg1, np.ndarray):
                self.shape = arg1.shape
                super().__init__(arg1.dtype.type, self.shape, *args, **kwargs)
                self.data = arg1
                self._isnull = False
            else:
                raise TypeError
        else:
            self.shape = arg2
            super().__init__(arg1, self.shape, *args, **kwargs)
            self.data = np.empty(self.shape, self.dtype)
            self._isnull = True

    def set(self, val):
        try:
            self.data[...] = val
        except TypeError:
            self.data[...] = self._value_resolve(val)
        self.refresh()
    def rectify(self):
        if self._isnull:
            raise NullValueDetected
    def nullify(self):
        self._isnull = True

    @property
    def isnull(self):
        return self._isnull
