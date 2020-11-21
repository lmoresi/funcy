from ._base import Function
from .special import null
from .exceptions import *

class Slot(Function):

    def __init__(self, name = None):
        super().__init__(name = name)
    def _add_slots(self):
        self._slots = 1
        if self.name is None:
            self._argslots = 1
            self._kwargslots = []
        else:
            self._argslots = 0
            self._kwargslots = [self.name]
    def close(self, *args, **kwargs):
        if len(args) + len(kwargs) > self.slots:
            raise FuncyException
        if len(args):
            return args[0]
        elif len(kwargs):
            if not kwargs.keys()[0] == self.name:
                raise KeyError
            return kwargs.values()[0]
        else:
            raise Exception
        # raise FuncyException("Cannot close a Slot function.")
    def evaluate(self):
        return null
    @property
    def value(self):
        return null
