"""AGMAISO13281B14AccuracyGrader"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1189,
)

_AGMAISO13281B14_ACCURACY_GRADER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "AGMAISO13281B14AccuracyGrader",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1183,
        _1184,
        _1190,
    )

    Self = TypeVar("Self", bound="AGMAISO13281B14AccuracyGrader")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAISO13281B14AccuracyGrader._Cast_AGMAISO13281B14AccuracyGrader",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAISO13281B14AccuracyGrader",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAISO13281B14AccuracyGrader:
    """Special nested class for casting AGMAISO13281B14AccuracyGrader to subclasses."""

    __parent__: "AGMAISO13281B14AccuracyGrader"

    @property
    def iso132812013_accuracy_grader(
        self: "CastSelf",
    ) -> "_1189.ISO132812013AccuracyGrader":
        return self.__parent__._cast(_1189.ISO132812013AccuracyGrader)

    @property
    def iso1328_accuracy_grader_common(
        self: "CastSelf",
    ) -> "_1190.ISO1328AccuracyGraderCommon":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1190,
        )

        return self.__parent__._cast(_1190.ISO1328AccuracyGraderCommon)

    @property
    def cylindrical_accuracy_grader_with_profile_form_and_slope(
        self: "CastSelf",
    ) -> "_1184.CylindricalAccuracyGraderWithProfileFormAndSlope":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1184,
        )

        return self.__parent__._cast(
            _1184.CylindricalAccuracyGraderWithProfileFormAndSlope
        )

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1183.CylindricalAccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1183,
        )

        return self.__parent__._cast(_1183.CylindricalAccuracyGrader)

    @property
    def agmaiso13281b14_accuracy_grader(
        self: "CastSelf",
    ) -> "AGMAISO13281B14AccuracyGrader":
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
class AGMAISO13281B14AccuracyGrader(_1189.ISO132812013AccuracyGrader):
    """AGMAISO13281B14AccuracyGrader

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMAISO13281B14_ACCURACY_GRADER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAISO13281B14AccuracyGrader":
        """Cast to another type.

        Returns:
            _Cast_AGMAISO13281B14AccuracyGrader
        """
        return _Cast_AGMAISO13281B14AccuracyGrader(self)
