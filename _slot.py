from ._base import Function
from .special import null
from .exceptions import *

class Slot(Function):

    open = True

    __slots__ = (
        'slots',
        'argslots',
        'kwargslots',
        )

    def __init__(self, name = None):

        super().__init__(name = name)
    def _add_slots(self):
        self.slots = 1
        if self.name is None:
            self.argslots = 1
            self.kwargslots = []
        else:
            self.argslots = 0
            self.kwargslots = [self.name]
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
        try:
            return self.tempVal
        except AttributeError:
            return null
    @property
    def value(self):
        return self.evaluate()

    # def evaluate(self):
    #     key = self.name
    #     try:
    #         try:
    #             if key is None:
    #                 return GLOBEKWARGS[key].pop()
    #             else:
    #                 return GLOBEKWARGS[key]
    #         except KeyError:
    #             return GLOBEKWARGS.setdefault(key, GLOBEKWARGS[None].pop())
    #     except IndexError:
    #         return null
