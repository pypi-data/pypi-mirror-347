"""ShaftModalComplexShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4119
from mastapy._private.utility.units_and_measurements.measurements import _1746

_SHAFT_MODAL_COMPLEX_SHAPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "ShaftModalComplexShape",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
        _4122,
        _4123,
    )

    Self = TypeVar("Self", bound="ShaftModalComplexShape")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftModalComplexShape._Cast_ShaftModalComplexShape"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftModalComplexShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftModalComplexShape:
    """Special nested class for casting ShaftModalComplexShape to subclasses."""

    __parent__: "ShaftModalComplexShape"

    @property
    def shaft_complex_shape(self: "CastSelf") -> "_4119.ShaftComplexShape":
        return self.__parent__._cast(_4119.ShaftComplexShape)

    @property
    def shaft_modal_complex_shape_at_speeds(
        self: "CastSelf",
    ) -> "_4122.ShaftModalComplexShapeAtSpeeds":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4122,
        )

        return self.__parent__._cast(_4122.ShaftModalComplexShapeAtSpeeds)

    @property
    def shaft_modal_complex_shape_at_stiffness(
        self: "CastSelf",
    ) -> "_4123.ShaftModalComplexShapeAtStiffness":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4123,
        )

        return self.__parent__._cast(_4123.ShaftModalComplexShapeAtStiffness)

    @property
    def shaft_modal_complex_shape(self: "CastSelf") -> "ShaftModalComplexShape":
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
class ShaftModalComplexShape(_4119.ShaftComplexShape[_1746.Number, _1746.Number]):
    """ShaftModalComplexShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MODAL_COMPLEX_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftModalComplexShape":
        """Cast to another type.

        Returns:
            _Cast_ShaftModalComplexShape
        """
        return _Cast_ShaftModalComplexShape(self)
