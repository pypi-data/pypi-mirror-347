"""ProfileSlopeReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1172

_PROFILE_SLOPE_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "ProfileSlopeReliefWithDeviation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1174

    Self = TypeVar("Self", bound="ProfileSlopeReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ProfileSlopeReliefWithDeviation._Cast_ProfileSlopeReliefWithDeviation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileSlopeReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileSlopeReliefWithDeviation:
    """Special nested class for casting ProfileSlopeReliefWithDeviation to subclasses."""

    __parent__: "ProfileSlopeReliefWithDeviation"

    @property
    def profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1172.ProfileReliefWithDeviation":
        return self.__parent__._cast(_1172.ProfileReliefWithDeviation)

    @property
    def relief_with_deviation(self: "CastSelf") -> "_1174.ReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1174

        return self.__parent__._cast(_1174.ReliefWithDeviation)

    @property
    def profile_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "ProfileSlopeReliefWithDeviation":
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
class ProfileSlopeReliefWithDeviation(_1172.ProfileReliefWithDeviation):
    """ProfileSlopeReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_SLOPE_RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileSlopeReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_ProfileSlopeReliefWithDeviation
        """
        return _Cast_ProfileSlopeReliefWithDeviation(self)
