from collections.abc import Iterable, Iterator, Mapping
from functools import cached_property, lru_cache
import numbers

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

class Sample(Iterable, Function):
    @lru_cache
    def __getitem__(self, arg):
        if isinstance(arg, slice):
            return self._get_slice(arg.start, arg.stop, arg.step)
        else:
            return self._get_index(arg)
    def _get_index(self, index):
        it, i = iter(self), -1
        while i < index:
            i += 1
            val = next(it)
        try:
            return val
        except NameError:
            raise IndexError
    def _get_slice(self, start, stop, step):
        step = 1 if step is None else step
        it, i = iter(self), -1
        out = []
        for si in range(start, stop, step):
            while not i == si:
                val = next(it)
                i += 1
            out.append(val)
        return out
    def _iter(self):
        raise MissingAsset
    def __iter__(self):
        return Sampler(self)
    @property
    def _length(self):
        raise MissingAsset

    # def __init__(self, *args):
    #     super().__init__(*args)
    # def _evaluate(self):
    #     raise EvaluationError
    # def _recharge(self):
    #     self.sample = self._iter()

class Sampler(Iterator):
    __slots__ = (
        'sample',
        '_iterator',
        )
    def __init__(self, sample):
        self.sample = sample
        self._iterator = sample._iter()
    def __iter__(self):
        return self
    def __next__(self):
        return next(self._iterator)

class Seeded:
    @cached_property
    def _startseed(self):
        return reseed.digits(12, seed = self.hashID)

class Discrete(Sample):
    @cached_property
    def _length(self):
        return len(self.terms)
class Single(Discrete):
    def _iter(self):
        yield self.prime
class Arbitrary(Discrete):
    def _iter(self):
        return iter(self.terms)
class Choice(Seeded, Discrete):
    def _iter(self):
        low, high, _ = self.terms
        seed = self._startseed
        samples = list(range(low, high + 1))
        while len(samples):
            yield samples.pop(reseed.randint(0, len(samples) - 1, seed = seed))
            seed += 1
class Regular(Discrete):
    def _iter(self):
        start, stop, step = self.terms
        for i in range(len(self)):
            yield min(start + i * step, stop)
    @cached_property
    def _length(self):
        start, stop, step = self.terms
        return int((stop - start) / step) + 1

class Continuous(Sample):
    @cached_property
    def _length(self):
        return inf
class Random(Seeded, Continuous):
    def _iter(self):
        start, stop, _ = self.terms
        seed = self._startseed
        while True:
            v = reseed.rangearr(start, stop, seed = seed)
            if not len(v.shape):
                v = process_scalar(v)
            yield v
            seed += 1
