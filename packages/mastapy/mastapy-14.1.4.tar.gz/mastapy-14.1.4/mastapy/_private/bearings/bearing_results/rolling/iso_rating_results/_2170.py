"""RollerISOTS162812008Results"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2168

_ROLLER_ISOTS162812008_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "RollerISOTS162812008Results",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2167,
    )

    Self = TypeVar("Self", bound="RollerISOTS162812008Results")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerISOTS162812008Results._Cast_RollerISOTS162812008Results",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerISOTS162812008Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerISOTS162812008Results:
    """Special nested class for casting RollerISOTS162812008Results to subclasses."""

    __parent__: "RollerISOTS162812008Results"

    @property
    def isots162812008_results(self: "CastSelf") -> "_2168.ISOTS162812008Results":
        return self.__parent__._cast(_2168.ISOTS162812008Results)

    @property
    def iso_results(self: "CastSelf") -> "_2167.ISOResults":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2167,
        )

        return self.__parent__._cast(_2167.ISOResults)

    @property
    def roller_isots162812008_results(
        self: "CastSelf",
    ) -> "RollerISOTS162812008Results":
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
class RollerISOTS162812008Results(_2168.ISOTS162812008Results):
    """RollerISOTS162812008Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_ISOTS162812008_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_inner_ring(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingOfABearingLaminaOfTheInnerRing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_outer_ring(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingOfABearingLaminaOfTheOuterRing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def equivalent_load_assuming_line_contacts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentLoadAssumingLineContacts"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RollerISOTS162812008Results":
        """Cast to another type.

        Returns:
            _Cast_RollerISOTS162812008Results
        """
        return _Cast_RollerISOTS162812008Results(self)
