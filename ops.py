from collections.abc import Mapping
from collections import OrderedDict
from functools import cached_property, lru_cache, wraps
import inspect

from ._operation import Operation

def op_wrap(func, *keys):
    @wraps(func)
    def subwrap(*args, **kwargs):
        return func(*args, **kwargs)
    subwrap.__name__ = '.'.join([
        *(k for k in keys if not k.startswith('_')),
        func.__name__,
        ])
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Operation(
            *args,
            op = subwrap,
            **kwargs
            )
    return wrapper

class Ops:
    __slots__ = ('source', 'keys', 'ismodule')
    def __init__(self, source, *keys):
        if inspect.ismodule(source):
            self.source = source
            self.ismodule = True
        elif isinstance(source, Mapping):
            self.source = OrderedDict()
            for k, v in source.items():
                if isinstance(v, Mapping) or inspect.ismodule(v):
                    self.source[k] = Ops(v, *(*keys, k))
                elif callable(v):
                    self.source[k] = v
                else:
                    raise TypeError(v, type(v))
            self.ismodule = False
        else:
            raise TypeError(source, type(source))
        self.keys = keys
    @lru_cache
    def __getitem__(self, key):
        try:
            if self.ismodule:
                try:
                    obj = getattr(self.source, key)
                except AttributeError:
                    raise KeyError
            else:
                obj = self.source[key]
            if type(obj) is Ops:
                return obj
            else:
                return op_wrap(obj, *self.keys)
        except KeyError:
            if self.ismodule:
                raise KeyError
            else:
                for v in self.source.values():
                    if type(v) is Ops:
                        try:
                            return v[key]
                        except KeyError:
                            pass
                raise KeyError
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __call__(self, key, *args, **kwargs):
        return self[key](*args, **kwargs)
