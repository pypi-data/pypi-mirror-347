"""Component"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.part_model import _2534

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1557, _1558
    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.connections_and_sockets import (
        _2333,
        _2335,
        _2354,
        _2359,
    )
    from mastapy._private.system_model.part_model import (
        _2499,
        _2500,
        _2503,
        _2506,
        _2509,
        _2511,
        _2512,
        _2516,
        _2517,
        _2519,
        _2526,
        _2527,
        _2528,
        _2530,
        _2532,
        _2535,
        _2537,
        _2538,
        _2544,
        _2546,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2649,
        _2652,
        _2655,
        _2658,
        _2660,
        _2662,
        _2669,
        _2671,
        _2678,
        _2681,
        _2682,
        _2683,
        _2685,
        _2687,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2638, _2639
    from mastapy._private.system_model.part_model.gears import (
        _2582,
        _2584,
        _2586,
        _2587,
        _2588,
        _2590,
        _2592,
        _2594,
        _2596,
        _2597,
        _2599,
        _2603,
        _2605,
        _2607,
        _2609,
        _2612,
        _2614,
        _2616,
        _2618,
        _2619,
        _2620,
        _2622,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2549

    Self = TypeVar("Self", bound="Component")
    CastSelf = TypeVar("CastSelf", bound="Component._Cast_Component")


__docformat__ = "restructuredtext en"
__all__ = ("Component",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Component:
    """Special nested class for casting Component to subclasses."""

    __parent__: "Component"

    @property
    def part(self: "CastSelf") -> "_2534.Part":
        return self.__parent__._cast(_2534.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2499.AbstractShaft":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2500.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2500

        return self.__parent__._cast(_2500.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2503.Bearing":
        from mastapy._private.system_model.part_model import _2503

        return self.__parent__._cast(_2503.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2506.Bolt":
        from mastapy._private.system_model.part_model import _2506

        return self.__parent__._cast(_2506.Bolt)

    @property
    def connector(self: "CastSelf") -> "_2511.Connector":
        from mastapy._private.system_model.part_model import _2511

        return self.__parent__._cast(_2511.Connector)

    @property
    def datum(self: "CastSelf") -> "_2512.Datum":
        from mastapy._private.system_model.part_model import _2512

        return self.__parent__._cast(_2512.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2516.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2516

        return self.__parent__._cast(_2516.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2517.FEPart":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.FEPart)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2519.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2519

        return self.__parent__._cast(_2519.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2526.MassDisc":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2527.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2527

        return self.__parent__._cast(_2527.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2528.Microphone":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.Microphone)

    @property
    def mountable_component(self: "CastSelf") -> "_2530.MountableComponent":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2532.OilSeal":
        from mastapy._private.system_model.part_model import _2532

        return self.__parent__._cast(_2532.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2535.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2537.PointLoad":
        from mastapy._private.system_model.part_model import _2537

        return self.__parent__._cast(_2537.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2538.PowerLoad":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2544.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2544

        return self.__parent__._cast(_2544.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2546.VirtualComponent":
        from mastapy._private.system_model.part_model import _2546

        return self.__parent__._cast(_2546.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2549.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2549

        return self.__parent__._cast(_2549.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2582.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2584.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2586.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2587.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2588.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2590.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2590

        return self.__parent__._cast(_2590.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2592.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2594.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2596.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2597.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2599.Gear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2603.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2605.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2607.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2609.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2612.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2614.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2614

        return self.__parent__._cast(_2614.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2616.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2616

        return self.__parent__._cast(_2616.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2618.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2618

        return self.__parent__._cast(_2618.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2619.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2619

        return self.__parent__._cast(_2619.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2620.WormGear":
        from mastapy._private.system_model.part_model.gears import _2620

        return self.__parent__._cast(_2620.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2622.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2622

        return self.__parent__._cast(_2622.ZerolBevelGear)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2638.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2638

        return self.__parent__._cast(_2638.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2639.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2639

        return self.__parent__._cast(_2639.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2649.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2652.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2655.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2655

        return self.__parent__._cast(_2655.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2658.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2660.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2662.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2662

        return self.__parent__._cast(_2662.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2669.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2671.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2678.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2678

        return self.__parent__._cast(_2678.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2681.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2681

        return self.__parent__._cast(_2681.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2682.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2682

        return self.__parent__._cast(_2682.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2683.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2683

        return self.__parent__._cast(_2683.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2685.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2685

        return self.__parent__._cast(_2685.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2687.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2687

        return self.__parent__._cast(_2687.TorqueConverterTurbine)

    @property
    def component(self: "CastSelf") -> "Component":
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
class Component(_2534.Part):
    """Component

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_modal_damping_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return temp

    @additional_modal_damping_ratio.setter
    @enforce_parameter_types
    def additional_modal_damping_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalModalDampingRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def polar_inertia(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PolarInertia")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @polar_inertia.setter
    @enforce_parameter_types
    def polar_inertia(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PolarInertia", value)

    @property
    def polar_inertia_for_synchroniser_sizing_only(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "PolarInertiaForSynchroniserSizingOnly"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @polar_inertia_for_synchroniser_sizing_only.setter
    @enforce_parameter_types
    def polar_inertia_for_synchroniser_sizing_only(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PolarInertiaForSynchroniserSizingOnly", value
        )

    @property
    def reason_mass_properties_are_unknown(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonMassPropertiesAreUnknown")

        if temp is None:
            return ""

        return temp

    @property
    def reason_mass_properties_are_zero(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonMassPropertiesAreZero")

        if temp is None:
            return ""

        return temp

    @property
    def translation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Translation")

        if temp is None:
            return ""

        return temp

    @property
    def transverse_inertia(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TransverseInertia")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @transverse_inertia.setter
    @enforce_parameter_types
    def transverse_inertia(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TransverseInertia", value)

    @property
    def x_axis(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XAxis")

        if temp is None:
            return ""

        return temp

    @property
    def y_axis(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YAxis")

        if temp is None:
            return ""

        return temp

    @property
    def z_axis(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZAxis")

        if temp is None:
            return ""

        return temp

    @property
    def coordinate_system_euler_angles(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystemEulerAngles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @coordinate_system_euler_angles.setter
    @enforce_parameter_types
    def coordinate_system_euler_angles(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "CoordinateSystemEulerAngles", value)

    @property
    def local_coordinate_system(self: "Self") -> "_1557.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalCoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def position(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Position")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @position.setter
    @enforce_parameter_types
    def position(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Position", value)

    @property
    def component_connections(self: "Self") -> "List[_2333.ComponentConnection]":
        """List[mastapy.system_model.connections_and_sockets.ComponentConnection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def available_socket_offsets(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AvailableSocketOffsets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    def centre_offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreOffset")

        if temp is None:
            return 0.0

        return temp

    @property
    def translation_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TranslationVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def x_axis_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XAxisVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def y_axis_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YAxisVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def z_axis_vector(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZAxisVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def can_connect_to(self: "Self", component: "Component") -> "bool":
        """bool

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CanConnectTo", component.wrapped if component else None
        )
        return method_result

    @enforce_parameter_types
    def can_delete_connection(self: "Self", connection: "_2335.Connection") -> "bool":
        """bool

        Args:
            connection (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "CanDeleteConnection",
            connection.wrapped if connection else None,
        )
        return method_result

    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "Component"
    ) -> "_2509.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connect_to_socket(
        self: "Self", socket: "_2359.Socket"
    ) -> "_2509.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_coordinate_system_editor(self: "Self") -> "_1558.CoordinateSystemEditor":
        """mastapy.math_utility.CoordinateSystemEditor"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateCoordinateSystemEditor"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def diameter_at_middle_of_connection(
        self: "Self", connection: "_2335.Connection"
    ) -> "float":
        """float

        Args:
            connection (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DiameterAtMiddleOfConnection",
            connection.wrapped if connection else None,
        )
        return method_result

    @enforce_parameter_types
    def diameter_of_socket_for(self: "Self", connection: "_2335.Connection") -> "float":
        """float

        Args:
            connection (mastapy.system_model.connections_and_sockets.Connection)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DiameterOfSocketFor",
            connection.wrapped if connection else None,
        )
        return method_result

    @enforce_parameter_types
    def is_coaxially_connected_to(self: "Self", component: "Component") -> "bool":
        """bool

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "IsCoaxiallyConnectedTo",
            component.wrapped if component else None,
        )
        return method_result

    @enforce_parameter_types
    def is_directly_connected_to(self: "Self", component: "Component") -> "bool":
        """bool

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "IsDirectlyConnectedTo",
            component.wrapped if component else None,
        )
        return method_result

    @enforce_parameter_types
    def is_directly_or_indirectly_connected_to(
        self: "Self", component: "Component"
    ) -> "bool":
        """bool

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "IsDirectlyOrIndirectlyConnectedTo",
            component.wrapped if component else None,
        )
        return method_result

    @enforce_parameter_types
    def move_all_concentric_parts_radially(
        self: "Self", delta_x: "float", delta_y: "float"
    ) -> "bool":
        """bool

        Args:
            delta_x (float)
            delta_y (float)
        """
        delta_x = float(delta_x)
        delta_y = float(delta_y)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MoveAllConcentricPartsRadially",
            delta_x if delta_x else 0.0,
            delta_y if delta_y else 0.0,
        )
        return method_result

    @enforce_parameter_types
    def move_along_axis(self: "Self", delta: "float") -> None:
        """Method does not return.

        Args:
            delta (float)
        """
        delta = float(delta)
        pythonnet_method_call(self.wrapped, "MoveAlongAxis", delta if delta else 0.0)

    @enforce_parameter_types
    def move_with_concentric_parts_to_new_origin(
        self: "Self", target_origin: "Vector3D"
    ) -> "bool":
        """bool

        Args:
            target_origin (Vector3D)
        """
        target_origin = conversion.mp_to_pn_vector3d(target_origin)
        method_result = pythonnet_method_call(
            self.wrapped, "MoveWithConcentricPartsToNewOrigin", target_origin
        )
        return method_result

    @enforce_parameter_types
    def possible_sockets_to_connect_with_component(
        self: "Self", component: "Component"
    ) -> "List[_2359.Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "PossibleSocketsToConnectWith",
                [_COMPONENT],
                component.wrapped if component else None,
            )
        )

    @enforce_parameter_types
    def possible_sockets_to_connect_with(
        self: "Self", socket: "_2359.Socket"
    ) -> "List[_2359.Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_overload(
                self.wrapped,
                "PossibleSocketsToConnectWith",
                [_SOCKET],
                socket.wrapped if socket else None,
            )
        )

    @enforce_parameter_types
    def set_position_and_axis_of_component_and_connected_components(
        self: "Self", origin: "Vector3D", z_axis: "Vector3D"
    ) -> "_2354.RealignmentResult":
        """mastapy.system_model.connections_and_sockets.RealignmentResult

        Args:
            origin (Vector3D)
            z_axis (Vector3D)
        """
        origin = conversion.mp_to_pn_vector3d(origin)
        z_axis = conversion.mp_to_pn_vector3d(z_axis)
        method_result = pythonnet_method_call(
            self.wrapped,
            "SetPositionAndAxisOfComponentAndConnectedComponents",
            origin,
            z_axis,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def set_position_and_rotation_of_component_and_connected_components(
        self: "Self", new_coordinate_system: "_1557.CoordinateSystem3D"
    ) -> "_2354.RealignmentResult":
        """mastapy.system_model.connections_and_sockets.RealignmentResult

        Args:
            new_coordinate_system (mastapy.math_utility.CoordinateSystem3D)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "SetPositionAndRotationOfComponentAndConnectedComponents",
            new_coordinate_system.wrapped if new_coordinate_system else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def set_position_of_component_and_connected_components(
        self: "Self", position: "Vector3D"
    ) -> "_2354.RealignmentResult":
        """mastapy.system_model.connections_and_sockets.RealignmentResult

        Args:
            position (Vector3D)
        """
        position = conversion.mp_to_pn_vector3d(position)
        method_result = pythonnet_method_call(
            self.wrapped, "SetPositionOfComponentAndConnectedComponents", position
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def socket_named(self: "Self", socket_name: "str") -> "_2359.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket_name (str)
        """
        socket_name = str(socket_name)
        method_result = pythonnet_method_call(
            self.wrapped, "SocketNamed", socket_name if socket_name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_connect_to(
        self: "Self", component: "Component", hint_offset: "float" = float("nan")
    ) -> "_2509.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
            hint_offset (float, optional)
        """
        hint_offset = float(hint_offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryConnectTo",
            component.wrapped if component else None,
            hint_offset if hint_offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Component":
        """Cast to another type.

        Returns:
            _Cast_Component
        """
        return _Cast_Component(self)
