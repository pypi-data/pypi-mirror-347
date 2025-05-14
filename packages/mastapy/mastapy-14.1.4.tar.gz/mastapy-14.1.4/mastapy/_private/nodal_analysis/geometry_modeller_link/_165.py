"""GeometryModellerAngleDimension"""

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
from mastapy._private.nodal_analysis.geometry_modeller_link import _163

_GEOMETRY_MODELLER_ANGLE_DIMENSION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerAngleDimension"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometryModellerAngleDimension")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometryModellerAngleDimension._Cast_GeometryModellerAngleDimension",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerAngleDimension",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerAngleDimension:
    """Special nested class for casting GeometryModellerAngleDimension to subclasses."""

    __parent__: "GeometryModellerAngleDimension"

    @property
    def base_geometry_modeller_dimension(
        self: "CastSelf",
    ) -> "_163.BaseGeometryModellerDimension":
        return self.__parent__._cast(_163.BaseGeometryModellerDimension)

    @property
    def geometry_modeller_angle_dimension(
        self: "CastSelf",
    ) -> "GeometryModellerAngleDimension":
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
class GeometryModellerAngleDimension(_163.BaseGeometryModellerDimension):
    """GeometryModellerAngleDimension

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_ANGLE_DIMENSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @angle.setter
    @enforce_parameter_types
    def angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Angle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryModellerAngleDimension":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerAngleDimension
        """
        return _Cast_GeometryModellerAngleDimension(self)
