from functools import partial

from itertools import product
# from collections.abc import Iterable

from ._seqiterable import SeqIterable

class Mangle:
    @classmethod
    def get_method(cls, seq, key):
        return partial(getattr(cls, key), seq)
    @classmethod
    def standardise(cls, seq):
        return (
            t if isinstance(t, SeqIterable) else (t,)
                for t in seq._resolve_terms()
            )
    @classmethod
    def permute(cls, seq):
        return product(*cls.standardise(seq))
    @classmethod
    def concatenate(cls, seq):
        for t in cls.standardise(seq):
            for i in t:
                yield i
    @classmethod
    def zip(cls, seq):
        return zip(*cls.standardise(seq))
    # @clasmethod
    # def
