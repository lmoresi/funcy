from functools import wraps

from ._base import Variable
from .exceptions import *

# def iop_wrap(func):
#     @wraps(func)
#     def wrapper(self, val):
#         try:
#             # func(self, self._value_resolve(val))
#             func(self, val)
#             # self.refresh()
#             return self
#         except AttributeError:
#             raise NullValueDetected
#     return wrapper

class Simple(Variable):
    def __iadd__(self, arg):
        self.data += arg
        self.refresh()
        return self
    def __isub__(self, arg):
        self.data -= arg
        self.refresh()
        return self
    def __imul__(self, arg):
        self.data *= arg
        self.refresh()
        return self
    def __itruediv__(self, arg):
        self.data /= arg
        self.refresh()
        return self
    def __ifloordiv__(self, arg):
        self.data //= arg
        self.refresh()
        return self
    def __imod__(self, arg):
        self.data %= arg
        self.refresh()
        return self
    def __ipow__(self, arg):
        self.data **= arg
        self.refresh()
        return self
