"""CylindricalAccuracyGraderWithProfileFormAndSlope"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1183,
)

_CYLINDRICAL_ACCURACY_GRADER_WITH_PROFILE_FORM_AND_SLOPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "CylindricalAccuracyGraderWithProfileFormAndSlope",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1179,
        _1181,
        _1188,
        _1189,
        _1190,
    )

    Self = TypeVar("Self", bound="CylindricalAccuracyGraderWithProfileFormAndSlope")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalAccuracyGraderWithProfileFormAndSlope._Cast_CylindricalAccuracyGraderWithProfileFormAndSlope",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalAccuracyGraderWithProfileFormAndSlope",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalAccuracyGraderWithProfileFormAndSlope:
    """Special nested class for casting CylindricalAccuracyGraderWithProfileFormAndSlope to subclasses."""

    __parent__: "CylindricalAccuracyGraderWithProfileFormAndSlope"

    @property
    def cylindrical_accuracy_grader(
        self: "CastSelf",
    ) -> "_1183.CylindricalAccuracyGrader":
        return self.__parent__._cast(_1183.CylindricalAccuracyGrader)

    @property
    def agma20151a01_accuracy_grader(
        self: "CastSelf",
    ) -> "_1179.AGMA20151A01AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1179,
        )

        return self.__parent__._cast(_1179.AGMA20151A01AccuracyGrader)

    @property
    def agmaiso13281b14_accuracy_grader(
        self: "CastSelf",
    ) -> "_1181.AGMAISO13281B14AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1181,
        )

        return self.__parent__._cast(_1181.AGMAISO13281B14AccuracyGrader)

    @property
    def iso132811995_accuracy_grader(
        self: "CastSelf",
    ) -> "_1188.ISO132811995AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1188,
        )

        return self.__parent__._cast(_1188.ISO132811995AccuracyGrader)

    @property
    def iso132812013_accuracy_grader(
        self: "CastSelf",
    ) -> "_1189.ISO132812013AccuracyGrader":
        from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
            _1189,
        )

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
    ) -> "CylindricalAccuracyGraderWithProfileFormAndSlope":
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
class CylindricalAccuracyGraderWithProfileFormAndSlope(_1183.CylindricalAccuracyGrader):
    """CylindricalAccuracyGraderWithProfileFormAndSlope

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_ACCURACY_GRADER_WITH_PROFILE_FORM_AND_SLOPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def helix_slope_deviation_per_inch_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixSlopeDeviationPerInchFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_pitches_for_sector_pitch_deviation(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPitchesForSectorPitchDeviation"
        )

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalAccuracyGraderWithProfileFormAndSlope":
        """Cast to another type.

        Returns:
            _Cast_CylindricalAccuracyGraderWithProfileFormAndSlope
        """
        return _Cast_CylindricalAccuracyGraderWithProfileFormAndSlope(self)
