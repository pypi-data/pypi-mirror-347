"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings import _1956

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_RollingBearingRaceType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_RollingBearingRaceType",)


class EnumWithSelectedValue_RollingBearingRaceType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_RollingBearingRaceType

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingRaceType' types.
    """

    __qualname__ = "RollingBearingRaceType"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_RollingBearingRaceType]",
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
        cls: "Type[EnumWithSelectedValue_RollingBearingRaceType]",
    ) -> "_1956.RollingBearingRaceType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1956.RollingBearingRaceType
        """
        return _1956.RollingBearingRaceType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_RollingBearingRaceType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1956.RollingBearingRaceType.type_()

    @property
    def selected_value(self: "Self") -> "_1956.RollingBearingRaceType":
        """mastapy.bearings.RollingBearingRaceType

        Note:
            This property is readonly.
        """
        return None

    @property
    def available_values(self: "Self") -> "List[_1956.RollingBearingRaceType]":
        """List[mastapy.bearings.RollingBearingRaceType]

        Note:
            This property is readonly.
        """
        return None
