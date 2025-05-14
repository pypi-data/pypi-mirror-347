"""CADFieldWindingSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1321

_CAD_FIELD_WINDING_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADFieldWindingSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CADFieldWindingSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CADFieldWindingSpecification._Cast_CADFieldWindingSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CADFieldWindingSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADFieldWindingSpecification:
    """Special nested class for casting CADFieldWindingSpecification to subclasses."""

    __parent__: "CADFieldWindingSpecification"

    @property
    def field_winding_specification_base(
        self: "CastSelf",
    ) -> "_1321.FieldWindingSpecificationBase":
        return self.__parent__._cast(_1321.FieldWindingSpecificationBase)

    @property
    def cad_field_winding_specification(
        self: "CastSelf",
    ) -> "CADFieldWindingSpecification":
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
class CADFieldWindingSpecification(_1321.FieldWindingSpecificationBase):
    """CADFieldWindingSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_FIELD_WINDING_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CADFieldWindingSpecification":
        """Cast to another type.

        Returns:
            _Cast_CADFieldWindingSpecification
        """
        return _Cast_CADFieldWindingSpecification(self)
