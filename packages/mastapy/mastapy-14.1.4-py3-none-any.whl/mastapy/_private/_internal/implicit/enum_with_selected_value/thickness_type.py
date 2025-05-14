"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1120

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ThicknessType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ThicknessType",)


class EnumWithSelectedValue_ThicknessType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThicknessType

    A specific implementation of 'EnumWithSelectedValue' for 'ThicknessType' types.
    """

    __qualname__ = "ThicknessType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ThicknessType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ThicknessType]",
    ) -> "_1120.ThicknessType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1120.ThicknessType
        """
        return _1120.ThicknessType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ThicknessType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1120.ThicknessType.type_()

    @property
    def selected_value(self: "Self") -> "_1120.ThicknessType":
        """mastapy.gears.gear_designs.cylindrical.ThicknessType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1120.ThicknessType]":
        """List[mastapy.gears.gear_designs.cylindrical.ThicknessType]

        Note:
            This property is readonly.
        """
        return None
