"""DynamicForceAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1410
from mastapy._private.electric_machines.results import _1397

_DYNAMIC_FORCE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "DynamicForceAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1404, _1414
    from mastapy._private.electric_machines.results import _1379

    Self = TypeVar("Self", bound="DynamicForceAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicForceAnalysis._Cast_DynamicForceAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicForceAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicForceAnalysis:
    """Special nested class for casting DynamicForceAnalysis to subclasses."""

    __parent__: "DynamicForceAnalysis"

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1410.ElectricMachineAnalysis":
        return self.__parent__._cast(_1410.ElectricMachineAnalysis)

    @property
    def dynamic_force_analysis(self: "CastSelf") -> "DynamicForceAnalysis":
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
class DynamicForceAnalysis(
    _1410.ElectricMachineAnalysis, _1397.IHaveDynamicForceResults
):
    """DynamicForceAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_FORCE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def number_of_steps_per_operating_point(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsPerOperatingPoint")

        if temp is None:
            return 0

        return temp

    @property
    def load_case(self: "Self") -> "_1404.BasicDynamicForceLoadCase":
        """mastapy.electric_machines.load_cases_and_analyses.BasicDynamicForceLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results(self: "Self") -> "_1379.DynamicForceResults":
        """mastapy.electric_machines.results.DynamicForceResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def single_operating_point_analyses(
        self: "Self",
    ) -> "List[_1414.ElectricMachineFEAnalysis]":
        """List[mastapy.electric_machines.load_cases_and_analyses.ElectricMachineFEAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleOperatingPointAnalyses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicForceAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicForceAnalysis
        """
        return _Cast_DynamicForceAnalysis(self)
