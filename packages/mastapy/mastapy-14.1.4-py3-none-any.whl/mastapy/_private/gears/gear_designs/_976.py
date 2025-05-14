"""DesignConstraint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.model_validation import _1851

_DESIGN_CONSTRAINT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "DesignConstraint"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar

    Self = TypeVar("Self", bound="DesignConstraint")
    CastSelf = TypeVar("CastSelf", bound="DesignConstraint._Cast_DesignConstraint")


__docformat__ = "restructuredtext en"
__all__ = ("DesignConstraint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignConstraint:
    """Special nested class for casting DesignConstraint to subclasses."""

    __parent__: "DesignConstraint"

    @property
    def design_constraint(self: "CastSelf") -> "DesignConstraint":
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
class DesignConstraint(_0.APIBase):
    """DesignConstraint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_CONSTRAINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def integer_range(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "IntegerRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @integer_range.setter
    @enforce_parameter_types
    def integer_range(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "IntegerRange", value)

    @property
    def property_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Property")

        if temp is None:
            return ""

        return temp

    @property
    def range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]"""
        temp = pythonnet_property_get(self.wrapped, "Range")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @range.setter
    @enforce_parameter_types
    def range(self: "Self", value: "Tuple[float, float]") -> None:
        value = conversion.mp_to_pn_range(value)
        pythonnet_property_set(self.wrapped, "Range", value)

    @property
    def severity(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_Severity":
        """EnumWithSelectedValue[mastapy.utility.model_validation.Severity]"""
        temp = pythonnet_property_get(self.wrapped, "Severity")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_Severity.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @severity.setter
    @enforce_parameter_types
    def severity(self: "Self", value: "_1851.Severity") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_Severity.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Severity", value)

    @property
    def type_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return ""

        return temp

    @property
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DesignConstraint":
        """Cast to another type.

        Returns:
            _Cast_DesignConstraint
        """
        return _Cast_DesignConstraint(self)
