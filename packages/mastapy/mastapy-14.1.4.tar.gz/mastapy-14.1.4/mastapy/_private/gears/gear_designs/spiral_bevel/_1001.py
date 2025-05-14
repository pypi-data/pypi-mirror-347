"""SpiralBevelGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.bevel import _1228

_SPIRAL_BEVEL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.SpiralBevel", "SpiralBevelGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _979, _980
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1241
    from mastapy._private.gears.gear_designs.conical import _1202

    Self = TypeVar("Self", bound="SpiralBevelGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearDesign._Cast_SpiralBevelGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearDesign:
    """Special nested class for casting SpiralBevelGearDesign to subclasses."""

    __parent__: "SpiralBevelGearDesign"

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1228.BevelGearDesign":
        return self.__parent__._cast(_1228.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1241.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1241

        return self.__parent__._cast(_1241.AGMAGleasonConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1202.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1202

        return self.__parent__._cast(_1202.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_979.GearDesign":
        from mastapy._private.gears.gear_designs import _979

        return self.__parent__._cast(_979.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _980

        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "SpiralBevelGearDesign":
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
class SpiralBevelGearDesign(_1228.BevelGearDesign):
    """SpiralBevelGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mean_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def recommended_maximum_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RecommendedMaximumFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearDesign":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearDesign
        """
        return _Cast_SpiralBevelGearDesign(self)
