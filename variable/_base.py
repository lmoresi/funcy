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
            initialValue = None,
            **kwargs,
            ):
        self.downstream = weakref.WeakSet()
        if not initialValue is None:
            self.set(initialValue)
        super().__init__(*args, **kwargs)

    def register_downstream(self, registrant):
        self.downstream.add(registrant)

    @cached_property
    def value(self):
        try:
            self._rectify()
            return self.data
        except (AttributeError, NullValueDetected):
            return null
    def set(self, val):
        self._set_value(val)
        self.refresh()
    def refresh(self):
        try:
            del self.value
            for down in self.downstream:
                down.update()
        except AttributeError:
            pass
    def nullify(self):
        self._nullify()
        self.refresh()

    def _set_value(self, val):
        self.data = val
    def _rectify(self):
        pass
    def _nullify(self):
        del self.data

# class Array(Function):
#
#     def __init__(self,
#             arg
#             ):
