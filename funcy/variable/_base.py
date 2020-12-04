from functools import cached_property
import weakref

from .._base import Function
from ..special import null
from .exceptions import *

class Variable(Function):

    open = False

    __slots__ = (
        'data',
        'downstream',
        )

    def __init__(self,
            *args,
            **kwargs,
            ):
        super().__init__(*args, **kwargs)
        self.downstream = weakref.WeakSet()
        self.data = null

    def register_downstream(self, registrant):
        self.downstream.add(registrant)

    @cached_property
    def value(self):
        self.rectify()
        return self.data
    def refresh(self):
        try:
            del self.value
        except AttributeError:
            pass
        for down in self.downstream:
            down.update()

    def set(self, val):
        raise MissingAsset
    def rectify(self):
        raise MissingAsset

# class Array(Function):
#
#     def __init__(self,
#             arg
#             ):
