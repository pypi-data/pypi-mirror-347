"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.detailed_rigid_connectors.splines import _1462

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_Modules")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_Modules",)


class EnumWithSelectedValue_Modules(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Modules

    A specific implementation of 'EnumWithSelectedValue' for 'Modules' types.
    """

    __qualname__ = "Modules"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_Modules]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls: "Type[EnumWithSelectedValue_Modules]") -> "_1462.Modules":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1462.Modules
        """
        return _1462.Modules

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_Modules]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1462.Modules.type_()

    @property
    def selected_value(self: "Self") -> "_1462.Modules":
        """mastapy.detailed_rigid_connectors.splines.Modules

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1462.Modules]":
        """List[mastapy.detailed_rigid_connectors.splines.Modules]

        Note:
            This property is readonly.
        """
        return None
