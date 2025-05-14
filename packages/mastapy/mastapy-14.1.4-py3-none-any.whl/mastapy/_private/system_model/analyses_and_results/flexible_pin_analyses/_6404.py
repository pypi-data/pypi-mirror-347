"""FlexiblePinAnalysisStopStartAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6398,
)

_FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisStopStartAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6397,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2878,
    )

    Self = TypeVar("Self", bound="FlexiblePinAnalysisStopStartAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAnalysisStopStartAnalysis._Cast_FlexiblePinAnalysisStopStartAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisStopStartAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisStopStartAnalysis:
    """Special nested class for casting FlexiblePinAnalysisStopStartAnalysis to subclasses."""

    __parent__: "FlexiblePinAnalysisStopStartAnalysis"

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "_6398.FlexiblePinAnalysis":
        return self.__parent__._cast(_6398.FlexiblePinAnalysis)

    @property
    def combination_analysis(self: "CastSelf") -> "_6397.CombinationAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6397,
        )

        return self.__parent__._cast(_6397.CombinationAnalysis)

    @property
    def flexible_pin_analysis_stop_start_analysis(
        self: "CastSelf",
    ) -> "FlexiblePinAnalysisStopStartAnalysis":
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
class FlexiblePinAnalysisStopStartAnalysis(_6398.FlexiblePinAnalysis):
    """FlexiblePinAnalysisStopStartAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def shaft_extreme_load_case(self: "Self") -> "_2878.ShaftSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftExtremeLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_nominal_load_case(self: "Self") -> "_2878.ShaftSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftNominalLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysisStopStartAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisStopStartAnalysis
        """
        return _Cast_FlexiblePinAnalysisStopStartAnalysis(self)
