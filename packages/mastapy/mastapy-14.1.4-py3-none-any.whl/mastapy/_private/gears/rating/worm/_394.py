"""WormGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _381

_WORM_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Worm", "WormGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1265
    from mastapy._private.gears.rating import _373

    Self = TypeVar("Self", bound="WormGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf", bound="WormGearSetDutyCycleRating._Cast_WormGearSetDutyCycleRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetDutyCycleRating:
    """Special nested class for casting WormGearSetDutyCycleRating to subclasses."""

    __parent__: "WormGearSetDutyCycleRating"

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_381.GearSetDutyCycleRating":
        return self.__parent__._cast(_381.GearSetDutyCycleRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_373.AbstractGearSetRating":
        from mastapy._private.gears.rating import _373

        return self.__parent__._cast(_373.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def worm_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "WormGearSetDutyCycleRating":
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
class WormGearSetDutyCycleRating(_381.GearSetDutyCycleRating):
    """WormGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetDutyCycleRating
        """
        return _Cast_WormGearSetDutyCycleRating(self)
