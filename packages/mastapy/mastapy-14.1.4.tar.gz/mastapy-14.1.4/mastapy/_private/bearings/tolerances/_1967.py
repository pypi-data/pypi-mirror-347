"""InnerRingTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.tolerances import _1978

_INNER_RING_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "InnerRingTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import _1962, _1970

    Self = TypeVar("Self", bound="InnerRingTolerance")
    CastSelf = TypeVar("CastSelf", bound="InnerRingTolerance._Cast_InnerRingTolerance")


__docformat__ = "restructuredtext en"
__all__ = ("InnerRingTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InnerRingTolerance:
    """Special nested class for casting InnerRingTolerance to subclasses."""

    __parent__: "InnerRingTolerance"

    @property
    def ring_tolerance(self: "CastSelf") -> "_1978.RingTolerance":
        return self.__parent__._cast(_1978.RingTolerance)

    @property
    def interference_tolerance(self: "CastSelf") -> "_1970.InterferenceTolerance":
        from mastapy._private.bearings.tolerances import _1970

        return self.__parent__._cast(_1970.InterferenceTolerance)

    @property
    def bearing_connection_component(
        self: "CastSelf",
    ) -> "_1962.BearingConnectionComponent":
        from mastapy._private.bearings.tolerances import _1962

        return self.__parent__._cast(_1962.BearingConnectionComponent)

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "InnerRingTolerance":
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
class InnerRingTolerance(_1978.RingTolerance):
    """InnerRingTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INNER_RING_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_InnerRingTolerance":
        """Cast to another type.

        Returns:
            _Cast_InnerRingTolerance
        """
        return _Cast_InnerRingTolerance(self)
