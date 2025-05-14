"""CylindricalGearSetMicroGeometryDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1278

_CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearSetMicroGeometryDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1265, _1274, _1277
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1140
    from mastapy._private.gears.gear_two_d_fe_analysis import _928
    from mastapy._private.gears.rating.cylindrical import _482

    Self = TypeVar("Self", bound="CylindricalGearSetMicroGeometryDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetMicroGeometryDutyCycle._Cast_CylindricalGearSetMicroGeometryDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetMicroGeometryDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetMicroGeometryDutyCycle:
    """Special nested class for casting CylindricalGearSetMicroGeometryDutyCycle to subclasses."""

    __parent__: "CylindricalGearSetMicroGeometryDutyCycle"

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1278.GearSetImplementationAnalysisDutyCycle":
        return self.__parent__._cast(_1278.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1277.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1277

        return self.__parent__._cast(_1277.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1274.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1274

        return self.__parent__._cast(_1274.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "CylindricalGearSetMicroGeometryDutyCycle":
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
class CylindricalGearSetMicroGeometryDutyCycle(
    _1278.GearSetImplementationAnalysisDutyCycle
):
    """CylindricalGearSetMicroGeometryDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "_482.CylindricalGearSetDutyCycleRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tiff_analysis(self: "Self") -> "_928.CylindricalGearSetTIFFAnalysisDutyCycle":
        """mastapy.gears.gear_two_d_fe_analysis.CylindricalGearSetTIFFAnalysisDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def meshes(self: "Self") -> "List[_1140.CylindricalGearMeshMicroGeometryDutyCycle]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometryDutyCycle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Meshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetMicroGeometryDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetMicroGeometryDutyCycle
        """
        return _Cast_CylindricalGearSetMicroGeometryDutyCycle(self)
