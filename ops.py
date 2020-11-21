from collections.abc import Mapping
from collections import OrderedDict
from functools import cached_property, lru_cache, wraps, partial
import inspect

def op_wrap(func, *keys, opclass):
    @wraps(func)
    def subwrap(*args, **kwargs):
        return func(*args, **kwargs)
    subwrap.__name__ = '.'.join([
        *(k for k in keys if not k.startswith('_')),
        func.__name__,
        ])
    @wraps(func)
    def wrapper(*args, **kwargs):
        return opclass(
            *args,
            op = subwrap,
            **kwargs
            )
    return wrapper

class Ops:
    __slots__ = ('source', 'rawsource', 'keys', 'ismodule', 'opclass')
    def __init__(self, source, *keys, opclass):
        self.rawsource = source
        self.opclass = opclass
        if inspect.ismodule(source):
            self.source = source
            self.ismodule = True
        elif isinstance(source, Mapping):
            self.source = OrderedDict()
            for k, v in source.items():
                if isinstance(v, Mapping) or inspect.ismodule(v):
                    self.source[k] = Ops(
                        v,
                        *(*keys, k),
                        opclass = self.opclass,
                        )
                elif callable(v):
                    self.source[k] = v
                else:
                    raise TypeError(v, type(v))
            self.ismodule = False
        else:
            raise TypeError(source, type(source))
        self.keys = keys
    def __getitem__(self, key):
        if type(key) is tuple:
            targ = self
            for k in key:
                targ = targ[k]
            return targ
        else:
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
                    return op_wrap(
                        obj,
                        *self.keys,
                        opclass = self.opclass
                        )
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

def getitem(x, y):
    return x[y]
def call(x, y):
    return x(y)
def amp(x, y):
    return x and y
def bar(x, y):
    return x or y
def hat(x, y):
    return (x or y) and not (x and y)


import math
import builtins
import operator
import itertools
import numpy
import scipy
import sklearn
makeops = partial(
    Ops,
    OrderedDict(
        _basic = dict(
            getitem = getitem,
            call = call,
            amp = amp,
            bar = bar,
            hat = hat,
            ),
        _builtins = builtins,
        _operator = operator,
        _math = math,
        _itertools = itertools,
        np = numpy,
        sp = scipy,
        sk = sklearn,
        ),
    )
