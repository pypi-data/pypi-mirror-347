"""ZerolBevelGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.bevel import _1230

_ZEROL_BEVEL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.ZerolBevel", "ZerolBevelGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _370
    from mastapy._private.gears.gear_designs import _980, _982
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1243
    from mastapy._private.gears.gear_designs.conical import _1204
    from mastapy._private.gears.gear_designs.zerol_bevel import _984, _985

    Self = TypeVar("Self", bound="ZerolBevelGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelGearSetDesign._Cast_ZerolBevelGearSetDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSetDesign:
    """Special nested class for casting ZerolBevelGearSetDesign to subclasses."""

    __parent__: "ZerolBevelGearSetDesign"

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1230.BevelGearSetDesign":
        return self.__parent__._cast(_1230.BevelGearSetDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1243.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1243

        return self.__parent__._cast(_1243.AGMAGleasonConicalGearSetDesign)

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
    def zerol_bevel_gear_set_design(self: "CastSelf") -> "ZerolBevelGearSetDesign":
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
class ZerolBevelGearSetDesign(_1230.BevelGearSetDesign):
    """ZerolBevelGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def minimum_number_of_teeth_for_recommended_tooth_proportions(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfTeethForRecommendedToothProportions"
        )

        if temp is None:
            return 0

        return temp

    @property
    def tooth_taper_zerol(self: "Self") -> "_370.ZerolBevelGleasonToothTaperOption":
        """mastapy.gears.ZerolBevelGleasonToothTaperOption"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperZerol")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.ZerolBevelGleasonToothTaperOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._370", "ZerolBevelGleasonToothTaperOption"
        )(value)

    @tooth_taper_zerol.setter
    @enforce_parameter_types
    def tooth_taper_zerol(
        self: "Self", value: "_370.ZerolBevelGleasonToothTaperOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.ZerolBevelGleasonToothTaperOption"
        )
        pythonnet_property_set(self.wrapped, "ToothTaperZerol", value)

    @property
    def gears(self: "Self") -> "List[_984.ZerolBevelGearDesign]":
        """List[mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign]

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
    def zerol_bevel_gears(self: "Self") -> "List[_984.ZerolBevelGearDesign]":
        """List[mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes(self: "Self") -> "List[_985.ZerolBevelGearMeshDesign]":
        """List[mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSetDesign
        """
        return _Cast_ZerolBevelGearSetDesign(self)
