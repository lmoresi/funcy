from collections.abc import Iterable, Iterator, Mapping
from functools import cached_property, lru_cache
import numbers
import weakref

import numpy as np

import reseed

from ._base import Function
from .special import *
from .exceptions import *

def process_scalar(scal):
    return scal.dtype.type(scal)

class Furcation:
    pass
    # def __init__(self, n):
    #     self.n = n
    # def __eq__(self, arg):
    #     return self.arg == self.n


class Seq(Function):
    discrete = True
    def _iter(self):
        return iter(self.prime)
    @cached_property
    def _seqLength(self):
        return len(self.prime)
    @cached_property
    def sub(self):
        return SubSeq(self)
    def _evaluate(self):
        return SeqIterable(self)

# class Gen(Seq):
#     def __init__()

class Seeded:
    @cached_property
    def _startseed(self):
        return reseed.digits(12, self.terms[2])

class RandomSeq(Seeded, Seq):
    @cached_property
    def _seqLength(self):
        return len(self._get_iterItems())
    def _iter(self):
        seed = self._startseed
        items = self._get_iterItems()
        while len(items):
            yield items.pop(
                reseed.randint(0, len(items) - 1, seed = seed)
                )
            seed += 1
    def _get_iterItems(self):
        return list(range(low, high + 1))

class PeriodicSeq(Seq):
    def __init__(self, start, stop, step = None, **kwargs):
        step = 1 if step is None else step
        if not isinstance(step, numbers.Number):
            raise FunctionCreationException
        super().__init__(start, stop, step, **kwargs)
    @cached_property
    def _seqLength(self):
        start, stop, step = self.terms
        return int((stop - start) / step) + 1
    def _iter(self):
        start, stop, step = self.terms
        for i in range(self._seqLength):
            yield min(start + i * step, stop)

class Continuum(Seq):
    discrete = False
    def __init__(self, start, stop, step = None, **kwargs):
        if any(isinstance(a, numbers.Integral) for a in (start, stop)):
            raise FunctionCreationException
        super().__init__(start, stop, step, **kwargs)
    @cached_property
    def _seqLength(self):
        return inf
    def _iter(self):
        start, stop, _ = self.terms
        seed = self._startseed
        while True:
            v = reseed.rangearr(start, stop, seed = seed)
            if not len(v.shape):
                v = process_scalar(v)
            yield v
            seed += 1

    # def __init__(self, *args):
    #     super().__init__(*args)
    # def _evaluate(self):
    #     raise EvaluationError
    # def _recharge(self):
    #     self.seq = self._iter()

class SubSeq:
    def __init__(self, seq):
        self._hostref = weakref.ref(seq)
    @property
    def seq(self):
        out = self._hostref()
        assert not out is None
        return out
    # def __getitem__

class SeqIterable(Iterable):
    __slots__ = (
        '_hostref',
        '_length',
        '__dict__',
        )
    def __init__(self, seq):
        self._hostref = weakref.ref(seq)
        self._length = seq._seqLength
    @property
    def seq(self):
        out = self._hostref()
        assert not out is None
        return out
    def __len__(self):
        return self._length
    def __iter__(self):
        return self.seq._iter()
    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return self._get_slice(*self._process_slice(arg))
        else:
            return self._get_index(arg)
    def _process_negative(self, target):
        if target < 0:
            if len(self) < inf:
                target = target + len(self)
            else:
                raise ValueError("Cannot reverse-index endless sequence.")
        return target
    def _process_slice(self, slicer):
        start, stop, step = slicer.start, slicer.stop, slicer.step
        return (
            self._process_negative(0 if start is None else start),
            self._process_negative(len(self) if stop is None else stop),
            (1 if step is None else step),
            )
    @lru_cache
    def _get_index(self, target):
        target = self._process_negative(target)
        it, i = iter(self), -1
        try:
            while i < target:
                i += 1
                val = next(it)
            try:
                return val
            except NameError:
                raise IndexError
        except StopIteration:
            raise IndexError
    @lru_cache
    def _get_slice(self, start, stop, step):
        return [self[i] for i in range(start, stop, step)]
        # it, i = iter(self), -1
        # out = []
        # for si in range(start, stop, step):
            # si = self._process_negative(si)
            # while not i == si:
            #     val = next(it)
            #     i += 1
            # out.append(val)
        # return out
    def __str__(self):
        return self._str
    @cached_property
    def _str(self):
        if len(self) < 10:
            content = ', '.join(str(v) for v in self)
        else:
            head = ', '.join(str(v) for v in self[:3])
            if len(self) < inf:
                tail = ', '.join(str(v) for v in self[-3:])
                content = f'{head}, ... {tail}'
            else:
                content = f'{head}, ... inf'
        return f'[{content}]'
    def __repr__(self):
        return self._repr
    @cached_property
    def _repr(self):
        return repr(self.seq) + ' == ' + str(self)

from ._fn import Fn
