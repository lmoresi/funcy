from collections import OrderedDict
from functools import cached_property, lru_cache

from .exceptions import *

class _Fn:
    @cached_property
    def op(self):
        from .ops import ops
        return ops
    @cached_property
    def elementop(self):
        from .ops import elementops
        return elementops
    @cached_property
    def seqop(self):
        from .ops import seqops
        return seqops
    @cached_property
    def base(self):
        from ._base import Function
        return Function
    @cached_property
    def var(self):
        from ._variable import MutableVariable
        return MutableVariable
    @cached_property
    def slot(self):
        from ._slot import Slot
        return Slot
    @cached_property
    def exc(self):
        from ._trier import Trier
        return Trier
    @cached_property
    def group(self):
        from ._group import Group
        return Group
    @cached_property
    def seq(self):
        from .seq import seq
        return seq
    @cached_property
    def unseq(self):
        from .seq import UnSeq
        return UnSeq
    @cached_property
    def thing(self):
        from ._thing import Thing
        return Thing
    @cached_property
    def map(self):
        from ._map import Map
        return Map
    @cached_property
    def inf(self):
        from .special import inf
        return inf
    @cached_property
    def ninf(self):
        from .special import ninf
        return ninf
    @cached_property
    def null(self):
        from .special import null
        return null
    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return self.slot(**kwargs)
        elif len(args) > 1:
            return self.group(*args, **kwargs)
        else:
            arg = args[0]
            if len(kwargs) == 0 and isinstance(arg, self.base):
                if arg.isSeq:
                    return self.unseq(arg)
                else:
                    return arg
            else:
                try:
                    return self.var(*args, **kwargs)
                except ValueError:
                    return self.thing(*args, **kwargs)
    def __getitem__(self, arg, **kwargs):
        return self.seq(arg, **kwargs)
    def __getattr__(self, key):
        return getattr(self.op, key)
Fn = _Fn()
