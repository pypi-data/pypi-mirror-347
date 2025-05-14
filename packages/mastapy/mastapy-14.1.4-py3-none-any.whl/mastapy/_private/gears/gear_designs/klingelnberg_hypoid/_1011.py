"""KlingelnbergCycloPalloidHypoidGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.klingelnberg_conical import _1015

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergHypoid",
    "KlingelnbergCycloPalloidHypoidGearSetDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _980, _982
    from mastapy._private.gears.gear_designs.conical import _1204
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1009, _1010

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetDesign._Cast_KlingelnbergCycloPalloidHypoidGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetDesign:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetDesign to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetDesign"

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1015.KlingelnbergConicalGearSetDesign":
        return self.__parent__._cast(_1015.KlingelnbergConicalGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1204.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1204

        return self.__parent__._cast(_1204.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_982.GearSetDesign":
        from mastapy._private.gears.gear_designs import _982

        return self.__parent__._cast(_982.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _980

        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetDesign":
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
class KlingelnbergCycloPalloidHypoidGearSetDesign(
    _1015.KlingelnbergConicalGearSetDesign
):
    """KlingelnbergCycloPalloidHypoidGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_face_width_on_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalFaceWidthOnPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    def angle_modification_applied_to_pinion(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleModificationAppliedToPinion")

        if temp is None:
            return 0.0

        return temp

    @angle_modification_applied_to_pinion.setter
    @enforce_parameter_types
    def angle_modification_applied_to_pinion(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleModificationAppliedToPinion",
            float(value) if value is not None else 0.0,
        )

    @property
    def angle_modification_applied_to_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleModificationAppliedToWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    def coasting_flank_normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoastingFlankNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @coasting_flank_normal_pressure_angle.setter
    @enforce_parameter_types
    def coasting_flank_normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoastingFlankNormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def cutter_blade_tip_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterBladeTipWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def driving_flank_normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DrivingFlankNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @driving_flank_normal_pressure_angle.setter
    @enforce_parameter_types
    def driving_flank_normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrivingFlankNormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def face_contact_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceContactAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def hw(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HW")

        if temp is None:
            return 0.0

        return temp

    @property
    def inner_offset_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerOffsetAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def inner_pitch_cone_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerPitchConeDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def inner_pitch_surface_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerPitchSurfaceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanNormalModule")

        if temp is None:
            return 0.0

        return temp

    @mean_normal_module.setter
    @enforce_parameter_types
    def mean_normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanNormalModule", float(value) if value is not None else 0.0
        )

    @property
    def mean_offset_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanOffsetAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_offset_angle_on_crown_wheel_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanOffsetAngleOnCrownWheelPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_addendum_modification_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAddendumModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def number_of_teeth_of_crown_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethOfCrownWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def offset_crown_wheel_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OffsetCrownWheelPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    def outer_offset_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterOffsetAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def partial_face_contact_angle_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartialFaceContactAngleA")

        if temp is None:
            return 0.0

        return temp

    @property
    def partial_face_contact_angle_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartialFaceContactAngleB")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_face_width_crown_wheel_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFaceWidthCrownWheelPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_face_width_inside_portion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFaceWidthInsidePortion")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_helix_angle_at_base_circle_of_virtual_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionHelixAngleAtBaseCircleOfVirtualGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_inner_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionMeanConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_outer_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionOuterConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def profile_contact_ratio_in_transverse_section_coasting_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileContactRatioInTransverseSectionCoastingFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def profile_contact_ratio_in_transverse_section_driving_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileContactRatioInTransverseSectionDrivingFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def respective_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RespectiveConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def settling_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SettlingAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def spiral_angle_at_inner_diameter_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralAngleAtInnerDiameterPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    def spiral_angle_at_outer_diameter_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralAngleAtOuterDiameterPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_tip_width_for_reduction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTipWidthForReduction")

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_pinion_teeth_at_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualNumberOfPinionTeethAtMeanConeDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def virtual_number_of_wheel_teeth_at_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VirtualNumberOfWheelTeethAtMeanConeDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_helix_angle_at_base_circle_of_virtual_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelHelixAngleAtBaseCircleOfVirtualGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_inner_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    def width_of_tooth_tip_chamfer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WidthOfToothTipChamfer")

        if temp is None:
            return 0.0

        return temp

    @property
    def gears(self: "Self") -> "List[_1009.KlingelnbergCycloPalloidHypoidGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears(
        self: "Self",
    ) -> "List[_1009.KlingelnbergCycloPalloidHypoidGearDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGears"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_conical_meshes(
        self: "Self",
    ) -> "List[_1010.KlingelnbergCycloPalloidHypoidGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes(
        self: "Self",
    ) -> "List[_1010.KlingelnbergCycloPalloidHypoidGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetDesign
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetDesign(self)
