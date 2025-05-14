"""ToothThicknessSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1127

_TOOTH_THICKNESS_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ToothThicknessSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1106

    Self = TypeVar("Self", bound="ToothThicknessSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothThicknessSpecification._Cast_ToothThicknessSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothThicknessSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothThicknessSpecification:
    """Special nested class for casting ToothThicknessSpecification to subclasses."""

    __parent__: "ToothThicknessSpecification"

    @property
    def tooth_thickness_specification_base(
        self: "CastSelf",
    ) -> "_1127.ToothThicknessSpecificationBase":
        return self.__parent__._cast(_1127.ToothThicknessSpecificationBase)

    @property
    def readonly_tooth_thickness_specification(
        self: "CastSelf",
    ) -> "_1106.ReadonlyToothThicknessSpecification":
        from mastapy._private.gears.gear_designs.cylindrical import _1106

        return self.__parent__._cast(_1106.ReadonlyToothThicknessSpecification)

    @property
    def tooth_thickness_specification(
        self: "CastSelf",
    ) -> "ToothThicknessSpecification":
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
class ToothThicknessSpecification(_1127.ToothThicknessSpecificationBase):
    """ToothThicknessSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_THICKNESS_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ToothThicknessSpecification":
        """Cast to another type.

        Returns:
            _Cast_ToothThicknessSpecification
        """
        return _Cast_ToothThicknessSpecification(self)
