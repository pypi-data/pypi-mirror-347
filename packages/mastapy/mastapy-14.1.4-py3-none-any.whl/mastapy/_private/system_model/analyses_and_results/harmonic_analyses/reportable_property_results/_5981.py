"""FEPartSingleWhineAnalysisResultsPropertyAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6001,
)

_FE_PART_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "FEPartSingleWhineAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _5977,
        _5995,
    )

    Self = TypeVar("Self", bound="FEPartSingleWhineAnalysisResultsPropertyAccessor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEPartSingleWhineAnalysisResultsPropertyAccessor._Cast_FEPartSingleWhineAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartSingleWhineAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartSingleWhineAnalysisResultsPropertyAccessor:
    """Special nested class for casting FEPartSingleWhineAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "FEPartSingleWhineAnalysisResultsPropertyAccessor"

    @property
    def single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6001.SingleWhineAnalysisResultsPropertyAccessor":
        return self.__parent__._cast(_6001.SingleWhineAnalysisResultsPropertyAccessor)

    @property
    def abstract_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_5977.AbstractSingleWhineAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _5977,
        )

        return self.__parent__._cast(
            _5977.AbstractSingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def fe_part_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "FEPartSingleWhineAnalysisResultsPropertyAccessor":
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
class FEPartSingleWhineAnalysisResultsPropertyAccessor(
    _6001.SingleWhineAnalysisResultsPropertyAccessor
):
    """FEPartSingleWhineAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def orders(self: "Self") -> "List[_5995.ResultsForOrderIncludingSurfaces]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingSurfaces]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Orders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_FEPartSingleWhineAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_FEPartSingleWhineAnalysisResultsPropertyAccessor
        """
        return _Cast_FEPartSingleWhineAnalysisResultsPropertyAccessor(self)
