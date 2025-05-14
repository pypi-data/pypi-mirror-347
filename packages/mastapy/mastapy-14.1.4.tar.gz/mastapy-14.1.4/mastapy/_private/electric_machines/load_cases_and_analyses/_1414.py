"""ElectricMachineFEAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1428
from mastapy._private.electric_machines.results import _1397

_ELECTRIC_MACHINE_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1410
    from mastapy._private.electric_machines.results import _1379
    from mastapy._private.nodal_analysis.elmer import _188

    Self = TypeVar("Self", bound="ElectricMachineFEAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineFEAnalysis._Cast_ElectricMachineFEAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineFEAnalysis:
    """Special nested class for casting ElectricMachineFEAnalysis to subclasses."""

    __parent__: "ElectricMachineFEAnalysis"

    @property
    def single_operating_point_analysis(
        self: "CastSelf",
    ) -> "_1428.SingleOperatingPointAnalysis":
        return self.__parent__._cast(_1428.SingleOperatingPointAnalysis)

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1410.ElectricMachineAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1410

        return self.__parent__._cast(_1410.ElectricMachineAnalysis)

    @property
    def electric_machine_fe_analysis(self: "CastSelf") -> "ElectricMachineFEAnalysis":
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
class ElectricMachineFEAnalysis(
    _1428.SingleOperatingPointAnalysis, _1397.IHaveDynamicForceResults
):
    """ElectricMachineFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def electromagnetic_solver_analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectromagneticSolverAnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_force_results(self: "Self") -> "_1379.DynamicForceResults":
        """mastapy.electric_machines.results.DynamicForceResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicForceResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def viewable(self: "Self") -> "_188.ElmerResultsViewable":
        """mastapy.nodal_analysis.elmer.ElmerResultsViewable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Viewable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineFEAnalysis
        """
        return _Cast_ElectricMachineFEAnalysis(self)
