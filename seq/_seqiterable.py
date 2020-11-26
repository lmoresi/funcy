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
        length = len(self)
        if isinstance(length, (Unknown, Infinite, Null)):
            raise ValueError("Cannot reverse this sequence.")
        return target + length
    def _process_slice(self, slicer):
        start, stop, step = slicer.start, slicer.stop, slicer.step
        return (
            0 if start is None else self._process_negative(start),
            len(self) if stop is None else self._process_negative(stop),
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
            raise IndexError(target)
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
        length = len(self)
        if isinstance(length, Infinite):
            head = ', '.join(str(v) for v in self[:3])
            content = f'{head}, ... inf'
        elif isinstance(length, Unknown):
            head = ', '.join(str(v) for v in self[:3])
            content = f'{head}, ... unk'
        else:
            if length < 10:
                content = ', '.join(str(v) for v in self)
            else:
                head = ', '.join(str(v) for v in self[:3])
                tail = ', '.join(str(v) for v in self[-3:])
                content = f'{head}, ... {tail}'
        return f'[{content}]'
    def __repr__(self):
        return f'SeqIterable({repr(self.seq)}) == {str(self)}'
