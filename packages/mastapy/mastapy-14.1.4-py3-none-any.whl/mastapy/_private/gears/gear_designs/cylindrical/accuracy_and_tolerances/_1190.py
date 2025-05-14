"""ISO1328AccuracyGraderCommon"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
    _1184,
)

_ISO1328_ACCURACY_GRADER_COMMON = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "ISO1328AccuracyGraderCommon",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances import (
        _1181,
        _1183,
        _1188,
        _1189,
        _1192,
    )

    Self = TypeVar("Self", bound="ISO1328AccuracyGraderCommon")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO1328AccuracyGraderCommon._Cast_ISO1328AccuracyGraderCommon",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO1328AccuracyGraderCommon",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO1328AccuracyGraderCommon:
    """Special nested class for casting ISO1328AccuracyGraderCommon to subclasses."""

    __parent__: "ISO1328AccuracyGraderCommon"

    @property
    def cylindrical_accuracy_grader_with_profile_form_and_slope(
        self: "CastSelf",
    ) -> "_1184.CylindricalAccuracyGraderWithProfileFormAndSlope":
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
    ) -> "ISO1328AccuracyGraderCommon":
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
class ISO1328AccuracyGraderCommon(
    _1184.CylindricalAccuracyGraderWithProfileFormAndSlope
):
    """ISO1328AccuracyGraderCommon

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO1328_ACCURACY_GRADER_COMMON

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def base_pitch_deviation(self: "Self") -> "_1192.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasePitchDeviation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def toothto_tooth_radial_composite_deviation(
        self: "Self",
    ) -> "_1192.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothtoToothRadialCompositeDeviation"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def total_radial_composite_deviation(self: "Self") -> "_1192.OverridableTolerance":
        """mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances.OverridableTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRadialCompositeDeviation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO1328AccuracyGraderCommon":
        """Cast to another type.

        Returns:
            _Cast_ISO1328AccuracyGraderCommon
        """
        return _Cast_ISO1328AccuracyGraderCommon(self)
