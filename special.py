from functools import wraps
import numbers

from .exceptions import *

class InfinInt(int):
    def __init__(self, pos = True):
        self._posArg = pos
        super().__init__()
    def _neg_inv(self, val):
        if self._posArg: return val
        else: return not val
    def _inf_comp(func):
        @wraps(func)
        def wrapper(self, arg):
            if isinstance(arg, InfinInt): return False
            else: return func(self, arg)
        return wrapper
    @_inf_comp
    def __eq__(self, arg): return False
    @_inf_comp
    def __ne__(self, arg): return True
    @_inf_comp
    def __lt__(self, arg): return self._neg_inv(False)
    @_inf_comp
    def __le__(self, arg): return self._neg_inv(False)
    @_inf_comp
    def __gt__(self, arg): return self._neg_inv(True)
    @_inf_comp
    def __ge__(self, arg): return self._neg_inv(True)
    @_inf_comp
    def __neg__(self, val): return ninf

    def __bool__(self, val): return self._posArg
    def __add__(self, arg): return self
    def __floordiv__(self, arg): return self
    def __truediv__(self, arg): return self
    def __mod__(self, arg): return self
    def __mul__(self, arg): return self
    def __pow__(self, arg): return self
    def __sub__(self, arg): return self
    def __truediv__(self, arg): return self

    def __index__(self):
        if self._posArg:
            return 999999999

    def __repr__(self):
        if self._posArg:
            return 'inf'
        else:
            return 'ninf'

inf = InfinInt(True)
ninf = InfinInt(False)

class Null(numbers.Number):

    def __getattr__(self, key): raise NullValueDetected
    def __getitem__(self, key): raise NullValueDetected
    def __setitem__(self, key, val): raise NullValueDetected

    def __add__(self, other): raise NullValueDetected
    def __sub__(self, other): raise NullValueDetected
    def __mul__(self, other): raise NullValueDetected
    def __matmul__(self, other): raise NullValueDetected
    def __truediv__(self, other): raise NullValueDetected
    def __floordiv__(self, other): raise NullValueDetected
    def __mod__(self, other): raise NullValueDetected
    def __divmod__(self, other): raise NullValueDetected
    def __pow__(self, other, modulo = None): raise NullValueDetected
    def __lshift__(self, other): raise NullValueDetected
    def __rshift__(self, other): raise NullValueDetected
    def __and__(self, other): raise NullValueDetected
    def __xor__(self, other): raise NullValueDetected
    def __or__(self, other): raise NullValueDetected

    def __radd__(self, other): raise NullValueDetected
    def __rsub__(self, other): raise NullValueDetected
    def __rmul__(self, other): raise NullValueDetected
    def __rmatmul__(self, other): raise NullValueDetected
    def __rtruediv__(self, other): raise NullValueDetected
    def __rfloordiv__(self, other): raise NullValueDetected
    def __rmod__(self, other): raise NullValueDetected
    def __rdivmod__(self, other): raise NullValueDetected
    def __rpow__(self, other, modulo = None): raise NullValueDetected
    def __rlshift__(self, other): raise NullValueDetected
    def __rrshift__(self, other): raise NullValueDetected
    def __rand__(self, other): raise NullValueDetected
    def __rxor__(self, other): raise NullValueDetected
    def __ror__(self, other): raise NullValueDetected

    def __iadd__(self, other): raise NullValueDetected
    def __isub__(self, other): raise NullValueDetected
    def __imul__(self, other): raise NullValueDetected
    def __imatmul__(self, other): raise NullValueDetected
    def __itruediv__(self, other): raise NullValueDetected
    def __ifloordiv__(self, other): raise NullValueDetected
    def __imod__(self, other): raise NullValueDetected
    def __ipow__(self, other, modulo = None): raise NullValueDetected
    def __ilshift__(self, other): raise NullValueDetected
    def __irshift__(self, other): raise NullValueDetected
    def __iand__(self, other): raise NullValueDetected
    def __ixor__(self, other): raise NullValueDetected
    def __ior__(self, other): raise NullValueDetected

    def __neg__(self): raise NullValueDetected
    def __pos__(self): raise NullValueDetected
    def __abs__(self): raise NullValueDetected
    def __invert__(self): raise NullValueDetected

    def __complex__(self): raise NullValueDetected
    def __int__(self): raise NullValueDetected
    def __float__(self): raise NullValueDetected

    def __index__(self): raise NullValueDetected # for integrals

    def __round__(self, ndigits = 0): raise NullValueDetected
    def __trunc__(self): raise NullValueDetected
    def __floor__(self): raise NullValueDetected
    def __ceil__(self): raise NullValueDetected

    def __coerce__ (self): raise NullValueDetected

null = Null()

# object.__add__(self, other)
# object.__sub__(self, other)
# object.__mul__(self, other)
# object.__matmul__(self, other)¶
# object.__truediv__(self, other)
# object.__floordiv__(self, other)
# object.__mod__(self, other)
# object.__divmod__(self, other)
# object.__pow__(self, other[, modulo])
# object.__lshift__(self, other)
# object.__rshift__(self, other)
# object.__and__(self, other)
# object.__xor__(self, other)
# object.__or__(self, other)
#
# object.__radd__(self, other)
# object.__rsub__(self, other)
# object.__rmul__(self, other)
# object.__rmatmul__(self, other)
# object.__rtruediv__(self, other)
# object.__rfloordiv__(self, other)
# object.__rmod__(self, other)
# object.__rdivmod__(self, other)
# object.__rpow__(self, other[, modulo])
# object.__rlshift__(self, other)
# object.__rrshift__(self, other)
# object.__rand__(self, other)
# object.__rxor__(self, other)
# object.__ror__(self, other)
#
# object.__iadd__(self, other)
# object.__isub__(self, other)
# object.__imul__(self, other)
# object.__imatmul__(self, other)
# object.__itruediv__(self, other)
# object.__ifloordiv__(self, other)
# object.__imod__(self, other)
# object.__ipow__(self, other[, modulo])
# object.__ilshift__(self, other)
# object.__irshift__(self, other)
# object.__iand__(self, other)
# object.__ixor__(self, other)
# object.__ior__(self, other)
#
# object.__neg__(self)
# object.__pos__(self)
# object.__abs__(self)
# object.__invert__(self)
#
# object.__complex__(self)
# object.__int__(self)
# object.__float__(self)
#
# object.__index__(self) # for integrals
#
# object.__round__(self[, ndigits])
# object.__trunc__(self)
# object.__floor__(self)
# object.__ceil__(self)
