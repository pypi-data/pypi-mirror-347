"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.micro_geometry import _593

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LocationOfEvaluationUpperLimit")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LocationOfEvaluationUpperLimit",)


class EnumWithSelectedValue_LocationOfEvaluationUpperLimit(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LocationOfEvaluationUpperLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationUpperLimit' types.
    """

    __qualname__ = "LocationOfEvaluationUpperLimit"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LocationOfEvaluationUpperLimit]",
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
        cls: "Type[EnumWithSelectedValue_LocationOfEvaluationUpperLimit]",
    ) -> "_593.LocationOfEvaluationUpperLimit":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _593.LocationOfEvaluationUpperLimit
        """
        return _593.LocationOfEvaluationUpperLimit

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LocationOfEvaluationUpperLimit]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _593.LocationOfEvaluationUpperLimit.type_()

    @property
    def selected_value(self: "Self") -> "_593.LocationOfEvaluationUpperLimit":
        """mastapy.gears.micro_geometry.LocationOfEvaluationUpperLimit

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_593.LocationOfEvaluationUpperLimit]":
        """List[mastapy.gears.micro_geometry.LocationOfEvaluationUpperLimit]

        Note:
            This property is readonly.
        """
        return None
