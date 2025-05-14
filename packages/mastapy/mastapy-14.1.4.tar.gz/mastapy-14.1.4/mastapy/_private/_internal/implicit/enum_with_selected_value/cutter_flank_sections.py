"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _640

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CutterFlankSections")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CutterFlankSections",)


class EnumWithSelectedValue_CutterFlankSections(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_CutterFlankSections

    A specific implementation of 'EnumWithSelectedValue' for 'CutterFlankSections' types.
    """

    __qualname__ = "CutterFlankSections"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_CutterFlankSections]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_CutterFlankSections]",
    ) -> "_640.CutterFlankSections":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _640.CutterFlankSections
        """
        return _640.CutterFlankSections

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_CutterFlankSections]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _640.CutterFlankSections.type_()

    @property
    def selected_value(self: "Self") -> "_640.CutterFlankSections":
        """mastapy.gears.manufacturing.cylindrical.CutterFlankSections

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_640.CutterFlankSections]":
        """List[mastapy.gears.manufacturing.cylindrical.CutterFlankSections]

        Note:
            This property is readonly.
        """
        return None
