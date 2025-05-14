"""BevelGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.agma_gleason_conical import _586

_BEVEL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel", "BevelGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1265
    from mastapy._private.gears.rating import _373, _382
    from mastapy._private.gears.rating.conical import _561
    from mastapy._private.gears.rating.spiral_bevel import _423
    from mastapy._private.gears.rating.straight_bevel import _416
    from mastapy._private.gears.rating.zerol_bevel import _390

    Self = TypeVar("Self", bound="BevelGearSetRating")
    CastSelf = TypeVar("CastSelf", bound="BevelGearSetRating._Cast_BevelGearSetRating")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetRating:
    """Special nested class for casting BevelGearSetRating to subclasses."""

    __parent__: "BevelGearSetRating"

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_586.AGMAGleasonConicalGearSetRating":
        return self.__parent__._cast(_586.AGMAGleasonConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_561.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _561

        return self.__parent__._cast(_561.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_382.GearSetRating":
        from mastapy._private.gears.rating import _382

        return self.__parent__._cast(_382.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_373.AbstractGearSetRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "_390.ZerolBevelGearSetRating":
        from mastapy._private.gears.rating.zerol_bevel import _390

        return self.__parent__._cast(_390.ZerolBevelGearSetRating)

    @property
    def straight_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_416.StraightBevelGearSetRating":
        from mastapy._private.gears.rating.straight_bevel import _416

        return self.__parent__._cast(_416.StraightBevelGearSetRating)

    @property
    def spiral_bevel_gear_set_rating(
        self: "CastSelf",
    ) -> "_423.SpiralBevelGearSetRating":
        from mastapy._private.gears.rating.spiral_bevel import _423

        return self.__parent__._cast(_423.SpiralBevelGearSetRating)

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "BevelGearSetRating":
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
class BevelGearSetRating(_586.AGMAGleasonConicalGearSetRating):
    """BevelGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetRating
        """
        return _Cast_BevelGearSetRating(self)
