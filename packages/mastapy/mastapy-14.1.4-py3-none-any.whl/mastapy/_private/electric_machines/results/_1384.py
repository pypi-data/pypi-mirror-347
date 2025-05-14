"""ElectricMachineResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELECTRIC_MACHINE_RESULTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "ElectricMachineResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1312, _1318
    from mastapy._private.electric_machines.results import (
        _1385,
        _1387,
        _1389,
        _1393,
        _1402,
        _1403,
    )
    from mastapy._private.utility_gui.charts import _1928

    Self = TypeVar("Self", bound="ElectricMachineResults")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineResults._Cast_ElectricMachineResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineResults:
    """Special nested class for casting ElectricMachineResults to subclasses."""

    __parent__: "ElectricMachineResults"

    @property
    def on_load_electric_machine_results(
        self: "CastSelf",
    ) -> "_1402.OnLoadElectricMachineResults":
        from mastapy._private.electric_machines.results import _1402

        return self.__parent__._cast(_1402.OnLoadElectricMachineResults)

    @property
    def open_circuit_electric_machine_results(
        self: "CastSelf",
    ) -> "_1403.OpenCircuitElectricMachineResults":
        from mastapy._private.electric_machines.results import _1403

        return self.__parent__._cast(_1403.OpenCircuitElectricMachineResults)

    @property
    def electric_machine_results(self: "CastSelf") -> "ElectricMachineResults":
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
class ElectricMachineResults(_0.APIBase):
    """ElectricMachineResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def average_d_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageDAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_q_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageQAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    def average_torque_mst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageTorqueMST")

        if temp is None:
            return 0.0

        return temp

    @property
    def eddy_current_loss_rotor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentLossRotor")

        if temp is None:
            return 0.0

        return temp

    @property
    def eddy_current_loss_stator_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentLossStatorTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def eddy_current_loss_stator_yoke(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentLossStatorYoke")

        if temp is None:
            return 0.0

        return temp

    @property
    def eddy_current_loss_stator(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentLossStator")

        if temp is None:
            return 0.0

        return temp

    @property
    def eddy_current_loss_total(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentLossTotal")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_loss_rotor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcessLossRotor")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_loss_stator_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcessLossStatorTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_loss_stator_yoke(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcessLossStatorYoke")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_loss_stator(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcessLossStator")

        if temp is None:
            return 0.0

        return temp

    @property
    def excess_loss_total(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcessLossTotal")

        if temp is None:
            return 0.0

        return temp

    @property
    def flux_density_in_air_gap_chart_at_time_0(
        self: "Self",
    ) -> "_1928.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluxDensityInAirGapChartAtTime0")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_density_in_air_gap_mst_chart_at_time_0(
        self: "Self",
    ) -> "_1928.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ForceDensityInAirGapMSTChartAtTime0"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hysteresis_loss_rotor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossRotor")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_stator_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossStatorTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_stator_yoke(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossStatorYoke")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_stator(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossStator")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_total(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossTotal")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_fundamental_rotor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossFundamentalRotor")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_fundamental_stator_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HysteresisLossFundamentalStatorTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_fundamental_stator_yoke(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HysteresisLossFundamentalStatorYoke"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_fundamental_stator(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossFundamentalStator")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_minor_loop_rotor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossMinorLoopRotor")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_minor_loop_stator_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HysteresisLossMinorLoopStatorTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_minor_loop_stator_yoke(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossMinorLoopStatorYoke")

        if temp is None:
            return 0.0

        return temp

    @property
    def hysteresis_loss_minor_loop_stator(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HysteresisLossMinorLoopStator")

        if temp is None:
            return 0.0

        return temp

    @property
    def magnet_loss_build_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ripple_mst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRippleMST")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_ac_winding_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalACWindingLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_core_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalCoreLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_magnet_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMagnetLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_rotor_core_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalRotorCoreLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_stator_core_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalStatorCoreLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_stator_teeth_iron_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalStatorTeethIronLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_stator_yoke_iron_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalStatorYokeIronLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def electric_machine_detail(self: "Self") -> "_1312.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def setup(self: "Self") -> "_1318.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_timesteps(self: "Self") -> "List[_1393.ElectricMachineResultsTimeStep]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsTimeStep]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsTimesteps")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def results_for_conductor_turns(
        self: "Self",
    ) -> "List[_1385.ElectricMachineResultsForConductorTurn]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsForConductorTurn]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForConductorTurns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def results_for_line_to_line(
        self: "Self",
    ) -> "List[_1387.ElectricMachineResultsForLineToLine]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsForLineToLine]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForLineToLine")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def results_for_phases(
        self: "Self",
    ) -> "List[_1389.ElectricMachineResultsForPhase]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsForPhase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForPhases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def results_for_this_and_slices(self: "Self") -> "List[ElectricMachineResults]":
        """List[mastapy.electric_machines.results.ElectricMachineResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForThisAndSlices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineResults":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineResults
        """
        return _Cast_ElectricMachineResults(self)
