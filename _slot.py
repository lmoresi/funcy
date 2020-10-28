from ._base import Function
from .exceptions import *

class Slot(Function):

    def __init__(self, name = None):
        self._slots = 1
        super().__init__()
        if not name is None:
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
            out = args[0]
        elif len(kwargs):
            if not kwargs.keys()[0] == self.name:
                raise KeyError
            out = kwargs.values()[0]
        return out
        # raise FunctionException("Cannot close a Slot function.")
