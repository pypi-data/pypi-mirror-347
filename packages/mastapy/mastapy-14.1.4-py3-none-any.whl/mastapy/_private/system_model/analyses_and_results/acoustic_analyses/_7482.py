"""HarmonicAcousticAnalysis"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_HARMONIC_ACOUSTIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "HarmonicAcousticAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.acoustic_analyses import (
        _7478,
        _7487,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5873,
        _5887,
        _5934,
    )
    from mastapy._private.utility import _1636

    Self = TypeVar("Self", bound="HarmonicAcousticAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicAcousticAnalysis._Cast_HarmonicAcousticAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAcousticAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAcousticAnalysis:
    """Special nested class for casting HarmonicAcousticAnalysis to subclasses."""

    __parent__: "HarmonicAcousticAnalysis"

    @property
    def harmonic_acoustic_analysis(self: "CastSelf") -> "HarmonicAcousticAnalysis":
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
class HarmonicAcousticAnalysis(_0.APIBase):
    """HarmonicAcousticAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ACOUSTIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def analysis_run_type(self: "Self") -> "_7478.AcousticAnalysisRunType":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.AcousticAnalysisRunType"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisRunType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.AcousticAnalysisRunType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7478",
            "AcousticAnalysisRunType",
        )(value)

    @analysis_run_type.setter
    @enforce_parameter_types
    def analysis_run_type(self: "Self", value: "_7478.AcousticAnalysisRunType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.AcousticAnalysisRunType",
        )
        pythonnet_property_set(self.wrapped, "AnalysisRunType", value)

    @property
    def number_of_frequencies_solved_for_last_run(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfFrequenciesSolvedForLastRun"
        )

        if temp is None:
            return 0

        return temp

    @property
    def analysis_run_information(self: "Self") -> "_1636.AnalysisRunInformation":
        """mastapy.utility.AnalysisRunInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisRunInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_frequency_options(
        self: "Self",
    ) -> "_5873.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisFrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_options(self: "Self") -> "_5887.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def reference_speed_options(
        self: "Self",
    ) -> "_5934.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def excitation_details_to_run(
        self: "Self",
    ) -> "List[_7487.SingleExcitationDetails]":
        """List[mastapy.system_model.analyses_and_results.acoustic_analyses.SingleExcitationDetails]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDetailsToRun")

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

    def calculate_boundary_surface_pressure(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateBoundarySurfacePressure")

    def clear_cached_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearCachedResults")

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
    def cast_to(self: "Self") -> "_Cast_HarmonicAcousticAnalysis":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAcousticAnalysis
        """
        return _Cast_HarmonicAcousticAnalysis(self)
