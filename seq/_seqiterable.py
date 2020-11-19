from collections.abc import Iterable
from functools import cached_property, lru_cache
import weakref
import itertools

from ..special import *
from .exceptions import *

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
        return self._length()
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
        return itertools.islice(self, start, stop, step)
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
        return f'SeqIterable({repr(self.seq)}) == {str(self)}'
