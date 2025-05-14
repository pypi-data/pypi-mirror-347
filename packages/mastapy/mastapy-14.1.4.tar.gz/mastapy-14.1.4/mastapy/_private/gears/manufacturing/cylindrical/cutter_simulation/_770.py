"""GearCutterSimulation"""

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

_GEAR_CUTTER_SIMULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "GearCutterSimulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
        _762,
        _765,
        _766,
        _767,
        _775,
        _778,
    )

    Self = TypeVar("Self", bound="GearCutterSimulation")
    CastSelf = TypeVar(
        "CastSelf", bound="GearCutterSimulation._Cast_GearCutterSimulation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearCutterSimulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearCutterSimulation:
    """Special nested class for casting GearCutterSimulation to subclasses."""

    __parent__: "GearCutterSimulation"

    @property
    def finish_cutter_simulation(self: "CastSelf") -> "_767.FinishCutterSimulation":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _767,
        )

        return self.__parent__._cast(_767.FinishCutterSimulation)

    @property
    def rough_cutter_simulation(self: "CastSelf") -> "_775.RoughCutterSimulation":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _775,
        )

        return self.__parent__._cast(_775.RoughCutterSimulation)

    @property
    def gear_cutter_simulation(self: "CastSelf") -> "GearCutterSimulation":
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
class GearCutterSimulation(_0.APIBase):
    """GearCutterSimulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_CUTTER_SIMULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def highest_finished_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestFinishedFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def least_sap_to_form_radius_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeastSAPToFormRadiusClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def lowest_finished_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestFinishedTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def average_thickness(self: "Self") -> "_762.CutterSimulationCalc":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def average_thickness_virtual(self: "Self") -> "_778.VirtualSimulationCalculator":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.VirtualSimulationCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageThicknessVirtual")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def least_profile(self: "Self") -> "_762.CutterSimulationCalc":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeastProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def least_profile_virtual(self: "Self") -> "_778.VirtualSimulationCalculator":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.VirtualSimulationCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeastProfileVirtual")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_thickness(self: "Self") -> "_762.CutterSimulationCalc":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_thickness_virtual(self: "Self") -> "_778.VirtualSimulationCalculator":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.VirtualSimulationCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumThicknessVirtual")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def minimum_thickness(self: "Self") -> "_762.CutterSimulationCalc":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def minimum_thickness_virtual(self: "Self") -> "_778.VirtualSimulationCalculator":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.VirtualSimulationCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumThicknessVirtual")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cutter_simulation(self: "Self") -> "GearCutterSimulation":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.GearCutterSimulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterSimulation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_mesh_cutter_simulations(
        self: "Self",
    ) -> "List[_765.CylindricalManufacturedRealGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedRealGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshCutterSimulations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gear_mesh_cutter_simulations_virtual(
        self: "Self",
    ) -> "List[_766.CylindricalManufacturedVirtualGearInMesh]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalManufacturedVirtualGearInMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshCutterSimulationsVirtual")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def thickness_calculators(self: "Self") -> "List[_762.CutterSimulationCalc]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.CutterSimulationCalc]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThicknessCalculators")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def virtual_thickness_calculators(
        self: "Self",
    ) -> "List[_778.VirtualSimulationCalculator]":
        """List[mastapy.gears.manufacturing.cylindrical.cutter_simulation.VirtualSimulationCalculator]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualThicknessCalculators")

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
    def cast_to(self: "Self") -> "_Cast_GearCutterSimulation":
        """Cast to another type.

        Returns:
            _Cast_GearCutterSimulation
        """
        return _Cast_GearCutterSimulation(self)
