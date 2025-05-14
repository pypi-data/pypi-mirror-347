"""ZerolBevelMeshedGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.bevel import _1231

_ZEROL_BEVEL_MESHED_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.ZerolBevel", "ZerolBevelMeshedGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _980
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1244
    from mastapy._private.gears.gear_designs.conical import _1207

    Self = TypeVar("Self", bound="ZerolBevelMeshedGearDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelMeshedGearDesign._Cast_ZerolBevelMeshedGearDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelMeshedGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelMeshedGearDesign:
    """Special nested class for casting ZerolBevelMeshedGearDesign to subclasses."""

    __parent__: "ZerolBevelMeshedGearDesign"

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1231.BevelMeshedGearDesign":
        return self.__parent__._cast(_1231.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1244.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1244

        return self.__parent__._cast(_1244.AGMAGleasonConicalMeshedGearDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1207.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1207

        return self.__parent__._cast(_1207.ConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_980.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _980

        return self.__parent__._cast(_980.GearDesignComponent)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "ZerolBevelMeshedGearDesign":
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
class ZerolBevelMeshedGearDesign(_1231.BevelMeshedGearDesign):
    """ZerolBevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_MESHED_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelMeshedGearDesign":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelMeshedGearDesign
        """
        return _Cast_ZerolBevelMeshedGearDesign(self)
