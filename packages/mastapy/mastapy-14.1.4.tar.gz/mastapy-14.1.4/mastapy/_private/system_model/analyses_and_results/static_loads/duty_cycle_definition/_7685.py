"""MultiTimeSeriesDataInputFileOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility_gui import _1909

_MULTI_TIME_SERIES_DATA_INPUT_FILE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "MultiTimeSeriesDataInputFileOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.file_access_helpers import _1879

    Self = TypeVar("Self", bound="MultiTimeSeriesDataInputFileOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MultiTimeSeriesDataInputFileOptions._Cast_MultiTimeSeriesDataInputFileOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultiTimeSeriesDataInputFileOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultiTimeSeriesDataInputFileOptions:
    """Special nested class for casting MultiTimeSeriesDataInputFileOptions to subclasses."""

    __parent__: "MultiTimeSeriesDataInputFileOptions"

    @property
    def data_input_file_options(self: "CastSelf") -> "_1909.DataInputFileOptions":
        return self.__parent__._cast(_1909.DataInputFileOptions)

    @property
    def multi_time_series_data_input_file_options(
        self: "CastSelf",
    ) -> "MultiTimeSeriesDataInputFileOptions":
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
class MultiTimeSeriesDataInputFileOptions(_1909.DataInputFileOptions):
    """MultiTimeSeriesDataInputFileOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTI_TIME_SERIES_DATA_INPUT_FILE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    def duration_scaling(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DurationScaling")

        if temp is None:
            return 0.0

        return temp

    @duration_scaling.setter
    @enforce_parameter_types
    def duration_scaling(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DurationScaling", float(value) if value is not None else 0.0
        )

    @property
    def proportion_of_duty_cycle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProportionOfDutyCycle")

        if temp is None:
            return 0.0

        return temp

    @proportion_of_duty_cycle.setter
    @enforce_parameter_types
    def proportion_of_duty_cycle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProportionOfDutyCycle",
            float(value) if value is not None else 0.0,
        )

    @property
    def delimiter_options(self: "Self") -> "_1879.TextFileDelimiterOptions":
        """mastapy.utility.file_access_helpers.TextFileDelimiterOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DelimiterOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MultiTimeSeriesDataInputFileOptions":
        """Cast to another type.

        Returns:
            _Cast_MultiTimeSeriesDataInputFileOptions
        """
        return _Cast_MultiTimeSeriesDataInputFileOptions(self)
