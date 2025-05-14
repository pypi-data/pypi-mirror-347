"""LeadReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1174

_LEAD_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "LeadReliefWithDeviation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1155,
        _1157,
        _1159,
        _1176,
    )

    Self = TypeVar("Self", bound="LeadReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf", bound="LeadReliefWithDeviation._Cast_LeadReliefWithDeviation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LeadReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LeadReliefWithDeviation:
    """Special nested class for casting LeadReliefWithDeviation to subclasses."""

    __parent__: "LeadReliefWithDeviation"

    @property
    def relief_with_deviation(self: "CastSelf") -> "_1174.ReliefWithDeviation":
        return self.__parent__._cast(_1174.ReliefWithDeviation)

    @property
    def lead_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1155.LeadFormReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1155

        return self.__parent__._cast(_1155.LeadFormReliefWithDeviation)

    @property
    def lead_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "_1157.LeadReliefSpecificationForCustomer102":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1157

        return self.__parent__._cast(_1157.LeadReliefSpecificationForCustomer102)

    @property
    def lead_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1159.LeadSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1159

        return self.__parent__._cast(_1159.LeadSlopeReliefWithDeviation)

    @property
    def total_lead_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1176.TotalLeadReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1176

        return self.__parent__._cast(_1176.TotalLeadReliefWithDeviation)

    @property
    def lead_relief_with_deviation(self: "CastSelf") -> "LeadReliefWithDeviation":
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
class LeadReliefWithDeviation(_1174.ReliefWithDeviation):
    """LeadReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEAD_RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def distance_along_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceAlongFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def lead_relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadRelief")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LeadReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_LeadReliefWithDeviation
        """
        return _Cast_LeadReliefWithDeviation(self)
