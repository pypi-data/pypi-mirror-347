"""GearSetLoadCaseBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1274

_GEAR_SET_LOAD_CASE_BASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase", "GearSetLoadCaseBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1265
    from mastapy._private.gears.load_case.bevel import _924
    from mastapy._private.gears.load_case.concept import _920
    from mastapy._private.gears.load_case.conical import _917
    from mastapy._private.gears.load_case.cylindrical import _914
    from mastapy._private.gears.load_case.face import _911
    from mastapy._private.gears.load_case.worm import _908

    Self = TypeVar("Self", bound="GearSetLoadCaseBase")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetLoadCaseBase._Cast_GearSetLoadCaseBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetLoadCaseBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetLoadCaseBase:
    """Special nested class for casting GearSetLoadCaseBase to subclasses."""

    __parent__: "GearSetLoadCaseBase"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1274.GearSetDesignAnalysis":
        return self.__parent__._cast(_1274.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1265.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1265

        return self.__parent__._cast(_1265.AbstractGearSetAnalysis)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_908.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _908

        return self.__parent__._cast(_908.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_911.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _911

        return self.__parent__._cast(_911.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_914.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _914

        return self.__parent__._cast(_914.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_917.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _917

        return self.__parent__._cast(_917.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_920.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _920

        return self.__parent__._cast(_920.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_924.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _924

        return self.__parent__._cast(_924.BevelSetLoadCase)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "GearSetLoadCaseBase":
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
class GearSetLoadCaseBase(_1274.GearSetDesignAnalysis):
    """GearSetLoadCaseBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_LOAD_CASE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def unit_duration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UnitDuration")

        if temp is None:
            return 0.0

        return temp

    @unit_duration.setter
    @enforce_parameter_types
    def unit_duration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UnitDuration", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetLoadCaseBase":
        """Cast to another type.

        Returns:
            _Cast_GearSetLoadCaseBase
        """
        return _Cast_GearSetLoadCaseBase(self)
