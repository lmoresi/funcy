from ._base import Function
from .exceptions import *

class Get(Function):

    def __init__(self,
            target,
            *keys,
            **kwargs,
            ):
        super().__init__(target, *keys, **kwargs)

    def _evaluate(self):
        target, *keys = self.terms
        target = self._value_resolve(target)
        for key in keys:
            key = self._value_resolve(key)
            target = self._evalget(target, key)
        return target

    def _evalget(self):
        raise MissingAsset

class GetAttr(Get):

    @staticmethod
    def _evalget(target, key):
        return getattr(target, prop)

class GetItem(Get):

    @staticmethod
    def _evalget(target, key):
        return target.__getitem__(prop)
