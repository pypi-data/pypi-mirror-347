"""ConceptGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _380

_CONCEPT_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Concept", "ConceptGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1263
    from mastapy._private.gears.gear_designs.concept import _1224
    from mastapy._private.gears.rating import _372, _377

    Self = TypeVar("Self", bound="ConceptGearRating")
    CastSelf = TypeVar("CastSelf", bound="ConceptGearRating._Cast_ConceptGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearRating:
    """Special nested class for casting ConceptGearRating to subclasses."""

    __parent__: "ConceptGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_380.GearRating":
        return self.__parent__._cast(_380.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_372.AbstractGearRating":
        from mastapy._private.gears.rating import _372

        return self.__parent__._cast(_372.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1263.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1263

        return self.__parent__._cast(_1263.AbstractGearAnalysis)

    @property
    def concept_gear_rating(self: "CastSelf") -> "ConceptGearRating":
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
class ConceptGearRating(_380.GearRating):
    """ConceptGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def concave_flank_rating(self: "Self") -> "_377.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConcaveFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def concept_gear(self: "Self") -> "_1224.ConceptGearDesign":
        """mastapy.gears.gear_designs.concept.ConceptGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def convex_flank_rating(self: "Self") -> "_377.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConvexFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearRating":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearRating
        """
        return _Cast_ConceptGearRating(self)
