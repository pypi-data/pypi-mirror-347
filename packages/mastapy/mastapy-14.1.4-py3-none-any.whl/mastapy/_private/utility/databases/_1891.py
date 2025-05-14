"""NamedKey"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _1887

_NAMED_KEY = python_net_import("SMT.MastaAPI.Utility.Databases", "NamedKey")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NamedKey")
    CastSelf = TypeVar("CastSelf", bound="NamedKey._Cast_NamedKey")


__docformat__ = "restructuredtext en"
__all__ = ("NamedKey",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedKey:
    """Special nested class for casting NamedKey to subclasses."""

    __parent__: "NamedKey"

    @property
    def database_key(self: "CastSelf") -> "_1887.DatabaseKey":
        return self.__parent__._cast(_1887.DatabaseKey)

    @property
    def named_key(self: "CastSelf") -> "NamedKey":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class NamedKey(_1887.DatabaseKey):
    """NamedKey

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_KEY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def cast_to(self: "Self") -> "_Cast_NamedKey":
        """Cast to another type.

        Returns:
            _Cast_NamedKey
        """
        return _Cast_NamedKey(self)
