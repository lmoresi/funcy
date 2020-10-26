from ._base import Function
from .exceptions import *

class Slot(Function):

    def __init__(self, name = None, dtype = None):
        self._slots = 1
        super().__init__(dtype = dtype)
        self._name = name
        if self.name is None:
            self._argslots = 1
            self._kwargslots = []
        else:
            self._argslots = 0
            self._kwargslots = [self.name]
    def close(self, *args, **kwargs):
        if len(args) + len(kwargs) > self._slots:
            raise FunctionException
        if len(args):
            return args[0]
        elif len(kwargs):
            if not kwargs.keys()[0] == self.name:
                raise KeyError
            return kwargs.values()[0]
        # raise FunctionException("Cannot close a Slot function.")
