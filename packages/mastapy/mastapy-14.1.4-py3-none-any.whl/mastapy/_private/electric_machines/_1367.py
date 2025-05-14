"""UShapedLayerSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1349

_U_SHAPED_LAYER_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "UShapedLayerSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.electric_machines import _1323, _1332, _1333, _1336

    Self = TypeVar("Self", bound="UShapedLayerSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="UShapedLayerSpecification._Cast_UShapedLayerSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UShapedLayerSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UShapedLayerSpecification:
    """Special nested class for casting UShapedLayerSpecification to subclasses."""

    __parent__: "UShapedLayerSpecification"

    @property
    def rotor_internal_layer_specification(
        self: "CastSelf",
    ) -> "_1349.RotorInternalLayerSpecification":
        return self.__parent__._cast(_1349.RotorInternalLayerSpecification)

    @property
    def u_shaped_layer_specification(self: "CastSelf") -> "UShapedLayerSpecification":
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
class UShapedLayerSpecification(_1349.RotorInternalLayerSpecification):
    """UShapedLayerSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _U_SHAPED_LAYER_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle_between_inner_and_outer_sections(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AngleBetweenInnerAndOuterSections")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angle_between_inner_and_outer_sections.setter
    @enforce_parameter_types
    def angle_between_inner_and_outer_sections(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AngleBetweenInnerAndOuterSections", value)

    @property
    def bridge_offset_above_layer_bend(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BridgeOffsetAboveLayerBend")

        if temp is None:
            return 0.0

        return temp

    @bridge_offset_above_layer_bend.setter
    @enforce_parameter_types
    def bridge_offset_above_layer_bend(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BridgeOffsetAboveLayerBend",
            float(value) if value is not None else 0.0,
        )

    @property
    def bridge_offset_below_layer_bend(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BridgeOffsetBelowLayerBend")

        if temp is None:
            return 0.0

        return temp

    @bridge_offset_below_layer_bend.setter
    @enforce_parameter_types
    def bridge_offset_below_layer_bend(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BridgeOffsetBelowLayerBend",
            float(value) if value is not None else 0.0,
        )

    @property
    def bridge_thickness_above_layer_bend(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BridgeThicknessAboveLayerBend")

        if temp is None:
            return 0.0

        return temp

    @bridge_thickness_above_layer_bend.setter
    @enforce_parameter_types
    def bridge_thickness_above_layer_bend(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BridgeThicknessAboveLayerBend",
            float(value) if value is not None else 0.0,
        )

    @property
    def bridge_thickness_below_layer_bend(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BridgeThicknessBelowLayerBend")

        if temp is None:
            return 0.0

        return temp

    @bridge_thickness_below_layer_bend.setter
    @enforce_parameter_types
    def bridge_thickness_below_layer_bend(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BridgeThicknessBelowLayerBend",
            float(value) if value is not None else 0.0,
        )

    @property
    def distance_between_inner_magnet_and_outer_flux_barrier(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceBetweenInnerMagnetAndOuterFluxBarrier"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_between_inner_magnet_and_outer_flux_barrier.setter
    @enforce_parameter_types
    def distance_between_inner_magnet_and_outer_flux_barrier(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceBetweenInnerMagnetAndOuterFluxBarrier",
            float(value) if value is not None else 0.0,
        )

    @property
    def distance_between_inner_magnets(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenInnerMagnets")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_inner_magnets.setter
    @enforce_parameter_types
    def distance_between_inner_magnets(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DistanceBetweenInnerMagnets", value)

    @property
    def distance_between_outer_magnet_and_inner_flux_barrier(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceBetweenOuterMagnetAndInnerFluxBarrier"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_between_outer_magnet_and_inner_flux_barrier.setter
    @enforce_parameter_types
    def distance_between_outer_magnet_and_inner_flux_barrier(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceBetweenOuterMagnetAndInnerFluxBarrier",
            float(value) if value is not None else 0.0,
        )

    @property
    def distance_between_outer_magnets_and_bridge(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceBetweenOuterMagnetsAndBridge"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_outer_magnets_and_bridge.setter
    @enforce_parameter_types
    def distance_between_outer_magnets_and_bridge(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DistanceBetweenOuterMagnetsAndBridge", value
        )

    @property
    def distance_to_layer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceToLayer")

        if temp is None:
            return 0.0

        return temp

    @distance_to_layer.setter
    @enforce_parameter_types
    def distance_to_layer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DistanceToLayer", float(value) if value is not None else 0.0
        )

    @property
    def flux_barrier_configuration(self: "Self") -> "_1323.FluxBarriers":
        """mastapy.electric_machines.FluxBarriers"""
        temp = pythonnet_property_get(self.wrapped, "FluxBarrierConfiguration")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.FluxBarriers"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1323", "FluxBarriers"
        )(value)

    @flux_barrier_configuration.setter
    @enforce_parameter_types
    def flux_barrier_configuration(self: "Self", value: "_1323.FluxBarriers") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.FluxBarriers"
        )
        pythonnet_property_set(self.wrapped, "FluxBarrierConfiguration", value)

    @property
    def inner_magnet_clearance(self: "Self") -> "_1332.MagnetClearance":
        """mastapy.electric_machines.MagnetClearance"""
        temp = pythonnet_property_get(self.wrapped, "InnerMagnetClearance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1332", "MagnetClearance"
        )(value)

    @inner_magnet_clearance.setter
    @enforce_parameter_types
    def inner_magnet_clearance(self: "Self", value: "_1332.MagnetClearance") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )
        pythonnet_property_set(self.wrapped, "InnerMagnetClearance", value)

    @property
    def magnet_configuration(self: "Self") -> "_1333.MagnetConfiguration":
        """mastapy.electric_machines.MagnetConfiguration"""
        temp = pythonnet_property_get(self.wrapped, "MagnetConfiguration")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.MagnetConfiguration"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1333", "MagnetConfiguration"
        )(value)

    @magnet_configuration.setter
    @enforce_parameter_types
    def magnet_configuration(self: "Self", value: "_1333.MagnetConfiguration") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.MagnetConfiguration"
        )
        pythonnet_property_set(self.wrapped, "MagnetConfiguration", value)

    @property
    def outer_magnet_lower_clearance(self: "Self") -> "_1332.MagnetClearance":
        """mastapy.electric_machines.MagnetClearance"""
        temp = pythonnet_property_get(self.wrapped, "OuterMagnetLowerClearance")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1332", "MagnetClearance"
        )(value)

    @outer_magnet_lower_clearance.setter
    @enforce_parameter_types
    def outer_magnet_lower_clearance(
        self: "Self", value: "_1332.MagnetClearance"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.MagnetClearance"
        )
        pythonnet_property_set(self.wrapped, "OuterMagnetLowerClearance", value)

    @property
    def thickness_of_inner_flux_barriers(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessOfInnerFluxBarriers")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thickness_of_inner_flux_barriers.setter
    @enforce_parameter_types
    def thickness_of_inner_flux_barriers(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThicknessOfInnerFluxBarriers", value)

    @property
    def thickness_of_outer_flux_barriers(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessOfOuterFluxBarriers")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thickness_of_outer_flux_barriers.setter
    @enforce_parameter_types
    def thickness_of_outer_flux_barriers(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThicknessOfOuterFluxBarriers", value)

    @property
    def web_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WebThickness")

        if temp is None:
            return 0.0

        return temp

    @web_thickness.setter
    @enforce_parameter_types
    def web_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WebThickness", float(value) if value is not None else 0.0
        )

    @property
    def outer_magnets(self: "Self") -> "_1336.MagnetForLayer":
        """mastapy.electric_machines.MagnetForLayer

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterMagnets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_UShapedLayerSpecification":
        """Cast to another type.

        Returns:
            _Cast_UShapedLayerSpecification
        """
        return _Cast_UShapedLayerSpecification(self)
