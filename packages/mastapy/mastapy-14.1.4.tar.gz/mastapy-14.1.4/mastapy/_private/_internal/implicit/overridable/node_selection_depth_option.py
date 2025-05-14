"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe import _2466

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_NodeSelectionDepthOption")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_NodeSelectionDepthOption",)


class Overridable_NodeSelectionDepthOption(mixins.OverridableMixin, Enum):
    """Overridable_NodeSelectionDepthOption

    A specific implementation of 'Overridable' for 'NodeSelectionDepthOption' types.
    """

    __qualname__ = "NodeSelectionDepthOption"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_NodeSelectionDepthOption]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_NodeSelectionDepthOption]",
    ) -> "_2466.NodeSelectionDepthOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2466.NodeSelectionDepthOption
        """
        return _2466.NodeSelectionDepthOption

    @classmethod
    def implicit_type(cls: "Type[Overridable_NodeSelectionDepthOption]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2466.NodeSelectionDepthOption.type_()

    @property
    def value(self: "Self") -> "_2466.NodeSelectionDepthOption":
        """mastapy.system_model.fe.NodeSelectionDepthOption

        Note:
            This property is readonly.
        """
        return None

    @property
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    def override_value(self: "Self") -> "_2466.NodeSelectionDepthOption":
        """mastapy.system_model.fe.NodeSelectionDepthOption

        Note:
            This property is readonly.
        """
        return None

    @property
    def calculated_value(self: "Self") -> "_2466.NodeSelectionDepthOption":
        """mastapy.system_model.fe.NodeSelectionDepthOption

        Note:
            This property is readonly.
        """
        return None
