from .._group import Group
from ._base import Seq
from .mangle import Mangle

class SeqGroup(Seq, Group):

    __slots__ = (
        '_iterTerms',
        )

    _defaultMangle = 'permute'

    def __init__(self, *args, mangle = None, **kwargs):
        if mangle is None:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(*args, mangle = mangle, **kwargs)
        mangle = self._defaultMangle if mangle is None else mangle
        self._iterTerms = Mangle.get_method(self, mangle)

    def _iter(self):
        return self._iterTerms()

    def mangle(self, key):
        return type(self)(*self.terms, **dict(**self.kwargs, mangle = key))
