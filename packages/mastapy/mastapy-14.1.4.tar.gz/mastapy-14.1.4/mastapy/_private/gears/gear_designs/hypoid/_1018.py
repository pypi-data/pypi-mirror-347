"""HypoidGearMeshDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1242

_HYPOID_GEAR_MESH_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Hypoid", "HypoidGearMeshDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _980, _981
    from mastapy._private.gears.gear_designs.conical import _1203
    from mastapy._private.gears.gear_designs.hypoid import _1017, _1019, _1020

    Self = TypeVar("Self", bound="HypoidGearMeshDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidGearMeshDesign._Cast_HypoidGearMeshDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearMeshDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearMeshDesign:
    """Special nested class for casting HypoidGearMeshDesign to subclasses."""

    __parent__: "HypoidGearMeshDesign"

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1242.AGMAGleasonConicalGearMeshDesign":
        return self.__parent__._cast(_1242.AGMAGleasonConicalGearMeshDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1203.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1203

        return self.__parent__._cast(_1203.ConicalGearMeshDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_981.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _981

        return self.__parent__._cast(_981.GearMeshDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _980

        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "HypoidGearMeshDesign":
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
class HypoidGearMeshDesign(_1242.AGMAGleasonConicalGearMeshDesign):
    """HypoidGearMeshDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_MESH_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def hypoid_gear_set(self: "Self") -> "_1019.HypoidGearSetDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hypoid_gears(self: "Self") -> "List[_1017.HypoidGearDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_meshed_gears(self: "Self") -> "List[_1020.HypoidMeshedGearDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidMeshedGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidMeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearMeshDesign":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearMeshDesign
        """
        return _Cast_HypoidGearMeshDesign(self)
