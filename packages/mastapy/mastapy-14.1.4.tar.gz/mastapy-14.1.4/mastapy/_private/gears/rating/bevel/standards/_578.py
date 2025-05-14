"""GleasonSpiralBevelGearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel.standards import _580

_GLEASON_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards",
    "GleasonSpiralBevelGearSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _383
    from mastapy._private.gears.rating.conical import _562

    Self = TypeVar("Self", bound="GleasonSpiralBevelGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GleasonSpiralBevelGearSingleFlankRating._Cast_GleasonSpiralBevelGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GleasonSpiralBevelGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GleasonSpiralBevelGearSingleFlankRating:
    """Special nested class for casting GleasonSpiralBevelGearSingleFlankRating to subclasses."""

    __parent__: "GleasonSpiralBevelGearSingleFlankRating"

    @property
    def spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_580.SpiralBevelGearSingleFlankRating":
        return self.__parent__._cast(_580.SpiralBevelGearSingleFlankRating)

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_562.ConicalGearSingleFlankRating":
        from mastapy._private.gears.rating.conical import _562

        return self.__parent__._cast(_562.ConicalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_383.GearSingleFlankRating":
        from mastapy._private.gears.rating import _383

        return self.__parent__._cast(_383.GearSingleFlankRating)

    @property
    def gleason_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "GleasonSpiralBevelGearSingleFlankRating":
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
class GleasonSpiralBevelGearSingleFlankRating(_580.SpiralBevelGearSingleFlankRating):
    """GleasonSpiralBevelGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GLEASON_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_scoring_index(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedScoringIndex")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_blank_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBlankTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    def hardness_ratio_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HardnessRatioFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def working_scoring_index(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingScoringIndex")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GleasonSpiralBevelGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_GleasonSpiralBevelGearSingleFlankRating
        """
        return _Cast_GleasonSpiralBevelGearSingleFlankRating(self)
