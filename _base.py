from functools import cached_property, lru_cache, wraps
import weakref
from collections.abc import Iterable, Sequence
from itertools import product

import numpy as np

from wordhash import w_hash
import reseed

from .exceptions import *

def convert(arg):
    try:
        return Fn(arg)
    except RedundantConvert:
        return arg

def refresh_wrap(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        out = func(self, *args, **kwargs)
        self.refresh()
        return out
    return wrapper

class Function(Sequence):

    __slots__ = (
        'terms',
        'keysDict',
        'kwargs',
        'prime',
        'downstream',
        '_slots',
        '_argslots',
        '_kwargslots',
        '__dict__',
        )

    def _value_resolve(self, val):
        while isinstance(val, Function):
            val = val.evaluate()
        return val

    def __init__(self, *terms, keys = dict(), **kwargs):
        self.terms = terms
        self.kwargs = kwargs
        self.downstream = weakref.WeakSet()
        if len(terms):
            self.prime = self.terms[0]
            for term in self.fnTerms:
                term.downstream.add(self)
        if len(keys):
            self.keysDict = keys

    @lru_cache(1)
    def evaluate(self):
        try:
            return self._evaluate()
        except Exception as e:
            if self.open:
                raise EvaluationError("Cannot evaluate open function.")
            # elif self.isiter:
            #     raise EvaluationError("Cannot evaluate iterable.")
            else:
                raise e
    def _evaluate(self):
        return iter(self)
    def refresh(self):
        self.evaluate.cache_clear()
        for down in self.downstream:
            down.refresh()
    @property
    def value(self):
        return self.evaluate()

    def _add_slots(self):
        self._argslots, self._kwargslots, self._slots = self._count_slots()
    def _count_slots(self):
        argslots = 0
        kwargslots = []
        for term in self.openTerms:
            if type(term) is Slot:
                if term.argslots:
                    argslots += 1
                elif not term.name in kwargslots:
                    kwargslots.append(term.name)
            else:
                kwargslots.extend(
                    k for k in term.kwargslots if not k in kwargslots
                    )
                argslots += term.argslots
        return argslots, kwargslots, argslots + len(kwargslots)
    @cached_property
    def fnTerms(self):
        return [t for t in self.terms if isinstance(t, Function)]
    @cached_property
    def openTerms(self):
        return [t for t in self.fnTerms if t.open]
    @cached_property
    def iterTerms(self):
        return [t for t in self.fnTerms if isinstance(t, Seq)]
    @cached_property
    def _termsAsIters(self):
        return [
            t.value if isinstance(t, Seq) else (t,)
                for t in self.terms
            ]
    @cached_property
    def isiter(self):
        return len(self.iterTerms)
    @cached_property
    def argslots(self):
        try:
            return self._argslots
        except AttributeError:
            self._add_slots()
            return self._argslots
    @cached_property
    def kwargslots(self):
        try:
            return self._kwargslots
        except AttributeError:
            self._add_slots()
            return self._kwargslots
    @cached_property
    def slots(self):
        try:
            return self._slots
        except AttributeError:
            self._add_slots()
            return self._slots
    @cached_property
    def open(self):
        return bool(self.slots)
    def allclose(self, arg):
        target = self
        while target.open:
            target = target.close(arg)
        assert not target.open
        return target
    @lru_cache()
    def close(self, *queryArgs, **queryKwargs):
        if not self.open:
            raise NothingToClose
        return self._close(*queryArgs, **queryKwargs)
    def _close(self,
            *queryArgs,
            **queryKwargs
            ):
        badKeys = [k for k in queryKwargs if not k in self.kwargslots]
        if badKeys:
            raise FunctionException("Inappropriate kwargs:", badKeys)
        unmatchedKwargs = [k for k in self.kwargslots if not k in queryKwargs]
        if len(queryArgs) > self.argslots and len(unmatchedKwargs):
            excessArgs = queryArgs[-(len(queryArgs) - self.argslots):]
            extraKwargs = dict(zip(self.kwargslots, excessArgs))
            excessArgs = excessArgs[len(extraKwargs):]
            if len(excessArgs):
                raise FunctionException("Too many args:", excessArgs)
            queryKwargs.update(extraKwargs)
        queryArgs = iter(queryArgs[:self.argslots])
        terms = []
        changes = 0
        for t in self.fnTerms:
            if type(t) is Slot:
                if t.argslots:
                    try:
                        t = next(queryArgs)
                        changes += 1
                    except StopIteration:
                        pass
                else:
                    if t.name in queryKwargs:
                        t = queryKwargs[t.name]
                        changes += 1
            else:
                if t.open:
                    queryArgs = list(queryArgs)
                    subArgs = queryArgs[:t.argslots]
                    leftovers = queryArgs[t.argslots:]
                    subKwargs = {
                        k: queryKwargs[k]
                            for k in queryKwargs if k in t.kwargslots
                        }
                    t = t.close(
                        *subArgs,
                        **subKwargs,
                        )
                    changes += 1
                    queryArgs = iter(leftovers)
            terms.append(t)
        if changes:
            outObj = type(self)(*terms, **self.kwargs)
        else:
            outObj = self
        return outObj
    def __call__(self, *args, **kwargs):
        if len(args) or len(kwargs):
            self = self.close(*args, **kwargs)
        return self.evaluate()

    @cached_property
    def get(self):
        return Getter(self)
    @lru_cache(32)
    def __getitem__(self, arg):
        try:
            return self.terms[arg]
        except TypeError:
            try:
                return self.terms[self.keysDict[arg]]
            except AttributeError:
                raise IndexError
    def __iter__(self):
        return iter(self.terms)
    def __len__(self):
        return self._length
    @cached_property
    def _length(self):
        return len(self.terms)

    @cached_property
    def name(self):
        try:
            return self.kwargs['name']
        except KeyError:
            return None

    @lru_cache
    def operate(self, *args, **kwargs):
        return self._operate(*args, **kwargs)
    def _operate(self, *args, op = None, truthy = False, **kwargs):
        return Operation(self, *args, op = op, **kwargs)

    def __add__(self, other): return self._operate(other, op = 'add')
    def __sub__(self, other):return self._operate(other, op = 'sub')
    def __mul__(self, other): return self._operate(other, op = 'mul')
    def __matmul__(self, other): return self._operate(other, op = 'matmul')
    def __truediv__(self, other): return self._operate(other, op = 'truediv')
    def __floordiv__(self, other): return self._operate(other, op = 'floordiv')
    def __mod__(self, other): return self._operate(other, op = 'mod')
    def __divmod__(self, other): return self._operate(other, op = 'divmod')
    def __pow__(self, other): return self._operate(other, op = 'pow')
    # def __lshift__(self, other): return self._operate(other, op = 'lshift')
    # def __rshift__(self, other): return self._operate(other, op = 'rshift')
    def __and__(self, other): return self._operate(other, op = 'all')
    # def __xor__(self, other):return self._operate(other, op = 'xor')
    def __or__(self, other): return self._operate(other, op = 'not')

    def __radd__(self, other): return self._operate(other, op = 'add')
    def __rsub__(self, other):return self._operate(other, op = 'sub')
    def __rmul__(self, other): return self._operate(other, op = 'mul')
    def __rmatmul__(self, other): return self._operate(other, op = 'matmul')
    def __rtruediv__(self, other): return self._operate(other, op = 'truediv')
    def __rfloordiv__(self, other): return self._operate(other, op = 'floordiv')
    def __rmod__(self, other): return self._operate(other, op = 'mod')
    def __rdivmod__(self, other): return self._operate(other, op = 'divmod')
    def __rpow__(self, other): return self._operate(other, op = 'pow')
    # def __rlshift__(self, other): return self._operate(other, op = 'lshift')
    # def __rrshift__(self, other): return self._operate(other, op = 'rshift')
    def __rand__(self, other): return self._operate(other, op = 'all')
    # def __rxor__(self, other):return self._operate(other, op = 'xor')
    def __ror__(self, other): return self._operate(other, op = 'any')

    def __neg__(self): return self._operate(op = 'neg')
    def __pos__(self): return self._operate(op = 'pos')
    def __abs__(self): return self._operate(op = 'abs')
    def __invert__(self): return self._operate(op = 'inv')

    # def __complex__(self): raise NullValueDetected
    # def __int__(self): raise NullValueDetected
    # def __float__(self): raise NullValueDetected
    #
    # def __index__(self): raise NullValueDetected # for integrals

    # def __round__(self, ndigits = 0): raise NullValueDetected
    # def __trunc__(self): raise NullValueDetected
    # def __floor__(self): raise NullValueDetected
    # def __ceil__(self): raise NullValueDetected

    def __bool__(self):
        return bool(self.value)
    def all(self):
        return Operation(*self.terms, op = 'all')
    def any(self):
        return Operation(*self.terms, op = 'any')

    def pipe_out(self, arg):
        raise NotYetImplemented

    @cached_property
    def namestr(self):
        return self._namestr()
    def _namestr(self):
        out = type(self).__name__ + self.kwargstr
        termstr = lambda t: t.namestr if hasattr(t, 'namestr') else str(t)
        if len(self.terms):
            termstr = ', '.join(termstr(t) for t in self.terms)
            out += '(' + termstr + ')'
        return out
    @cached_property
    def kwargstr(self):
        return self._kwargstr()
    def _kwargstr(self):
        outs = []
        for key, val in sorted(self.kwargs.items()):
            if not type(val) is str:
                if isinstance(val, Function):
                    val = val.namestr
                else:
                    try:
                        val = val.__name__
                    except AttributeError:
                        val = str(val)
            outs.append(': '.join((key, val)))
        return '{' + ', '.join(outs) + '}'

    @property
    def valstr(self):
        return self._valstr()
    def _valstr(self):
        if self.open:
            return 'open:' + str((self.argslots, self.kwargslots))
        else:
            try:
                return str(self.value)
            except (NullValueDetected, EvaluationError):
                return 'Null'
    def __repr__(self):
        return self.namestr
    def __str__(self):
        return ' == '.join([self.namestr, self.valstr])
    @cached_property
    def hashID(self):
        return w_hash(self.namestr)
    @cached_property
    def _hashInt(self):
        return reseed.digits(12, seed = self.hashID)
    def __hash__(self):
        return self._hashInt

    def op(self, arg, **kwargs):
        return self.operate(op = arg, **kwargs)

    def exc(self, exc = Exception, altVal = None):
        return Trier(self, exc = exc, altVal = altVal)

    def reduce(self, op = 'call'):
        target = self.terms[0]
        for term in self.terms[1:]:
            target = Fn(target, term).op(op)
        return target

class Getter(Sequence):
    def __init__(self, host):
        self.host = host
    def __call__(self, *args):
        return Fn(self.host, *keys).reduce(getattr)
    def __getitem__(self, arg):
        return Fn(self.host, arg).op('getitem')
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    def __len__(self):
        return len(self.host.value)

from ._operation import Operation, getop #, Boolean
from ._trier import Trier
from ._seq import Seq
from ._variable import Variable, MutableVariable
from ._thing import Thing
from ._slot import Slot
from ._fn import Fn
from ._seq import *


    # def __len__(self):
    #     return self._length
    # @cached_property
    # def _length(self):
    #     if self.isiter:
    #         v = 1
    #         for t in self.iterTerms:
    #             v *= len(val)
    #         return v
    #     else:
    #         return len(self.value)

        # if self.isiter:
        #     its = [
        #         [t,] if not isinstance(t, Iterable) else t
        #             for t in self.terms
        #         ]
        #     for args in product(*its):
        #         yield type(self)(*args, **self.kwargs)
        # else:
    # def __getitem__(self, key):
    #     if self.isiter:
    #         return Seq.__getitem__(self, key)
    #     else:
    #         if key >= len(self):
    #             raise IndexError
    #         return self.get[key]



    # @staticmethod
    # def bool(arg):
    #     return Operation(*args, op = bool)
    # @staticmethod
    # def all(*args):
    #     return Operation(*args, op = all)
    # @staticmethod
    # def any(*args):
    #     return Operation(*args, op = any)
    # @staticmethod
    # def not_fn(*args):
    #     return Operation(*args, op = bool, invert = True)
        # if type(arg) is list:
        #     try:
        #         arg = arg[0]
        #     except IndexError:
        #         arg = None
        #     outcls = ExtendableVariable
        # else:
        #     outcls = FixedVariable
        # arg = convert(arg)
        # if not isinstance(arg, FixedVariable):
        #     raise FunctionException(arg)
        # return outcls(self, **arg.kwargs)
    # def __rshift__(self, arg):
    #     return self.pipe_out(arg)
    # def __lshift__(self, arg):
    #     return arg.pipe_out(self)
