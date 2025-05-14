"""SKFCalculationResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SKF_CALCULATION_RESULT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "SKFCalculationResult"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import (
        _2138,
        _2140,
        _2141,
        _2142,
        _2143,
        _2145,
        _2148,
        _2149,
        _2150,
        _2151,
        _2152,
        _2153,
        _2161,
        _2162,
    )

    Self = TypeVar("Self", bound="SKFCalculationResult")
    CastSelf = TypeVar(
        "CastSelf", bound="SKFCalculationResult._Cast_SKFCalculationResult"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SKFCalculationResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SKFCalculationResult:
    """Special nested class for casting SKFCalculationResult to subclasses."""

    __parent__: "SKFCalculationResult"

    @property
    def adjusted_speed(self: "CastSelf") -> "_2138.AdjustedSpeed":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2138

        return self.__parent__._cast(_2138.AdjustedSpeed)

    @property
    def bearing_loads(self: "CastSelf") -> "_2140.BearingLoads":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2140

        return self.__parent__._cast(_2140.BearingLoads)

    @property
    def bearing_rating_life(self: "CastSelf") -> "_2141.BearingRatingLife":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2141

        return self.__parent__._cast(_2141.BearingRatingLife)

    @property
    def dynamic_axial_load_carrying_capacity(
        self: "CastSelf",
    ) -> "_2142.DynamicAxialLoadCarryingCapacity":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2142

        return self.__parent__._cast(_2142.DynamicAxialLoadCarryingCapacity)

    @property
    def frequencies(self: "CastSelf") -> "_2143.Frequencies":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2143

        return self.__parent__._cast(_2143.Frequencies)

    @property
    def friction(self: "CastSelf") -> "_2145.Friction":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2145

        return self.__parent__._cast(_2145.Friction)

    @property
    def grease(self: "CastSelf") -> "_2148.Grease":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2148

        return self.__parent__._cast(_2148.Grease)

    @property
    def grease_life_and_relubrication_interval(
        self: "CastSelf",
    ) -> "_2149.GreaseLifeAndRelubricationInterval":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2149

        return self.__parent__._cast(_2149.GreaseLifeAndRelubricationInterval)

    @property
    def grease_quantity(self: "CastSelf") -> "_2150.GreaseQuantity":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2150

        return self.__parent__._cast(_2150.GreaseQuantity)

    @property
    def initial_fill(self: "CastSelf") -> "_2151.InitialFill":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2151

        return self.__parent__._cast(_2151.InitialFill)

    @property
    def life_model(self: "CastSelf") -> "_2152.LifeModel":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2152

        return self.__parent__._cast(_2152.LifeModel)

    @property
    def minimum_load(self: "CastSelf") -> "_2153.MinimumLoad":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2153

        return self.__parent__._cast(_2153.MinimumLoad)

    @property
    def static_safety_factors(self: "CastSelf") -> "_2161.StaticSafetyFactors":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2161

        return self.__parent__._cast(_2161.StaticSafetyFactors)

    @property
    def viscosities(self: "CastSelf") -> "_2162.Viscosities":
        from mastapy._private.bearings.bearing_results.rolling.skf_module import _2162

        return self.__parent__._cast(_2162.Viscosities)

    @property
    def skf_calculation_result(self: "CastSelf") -> "SKFCalculationResult":
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
class SKFCalculationResult(_0.APIBase):
    """SKFCalculationResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SKF_CALCULATION_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_SKFCalculationResult":
        """Cast to another type.

        Returns:
            _Cast_SKFCalculationResult
        """
        return _Cast_SKFCalculationResult(self)
