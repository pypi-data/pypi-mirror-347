"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.enums import _1883

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection",)


class EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOptionFirstSelection' types.
    """

    __qualname__ = "ThreeDViewContourOptionFirstSelection"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection]",
    ) -> "_1883.ThreeDViewContourOptionFirstSelection":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1883.ThreeDViewContourOptionFirstSelection
        """
        return _1883.ThreeDViewContourOptionFirstSelection

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1883.ThreeDViewContourOptionFirstSelection.type_()

    @property
    def selected_value(self: "Self") -> "_1883.ThreeDViewContourOptionFirstSelection":
        """mastapy.utility.enums.ThreeDViewContourOptionFirstSelection

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(
        self: "Self",
    ) -> "List[_1883.ThreeDViewContourOptionFirstSelection]":
        """List[mastapy.utility.enums.ThreeDViewContourOptionFirstSelection]

        Note:
            This property is readonly.
        """
        return None
