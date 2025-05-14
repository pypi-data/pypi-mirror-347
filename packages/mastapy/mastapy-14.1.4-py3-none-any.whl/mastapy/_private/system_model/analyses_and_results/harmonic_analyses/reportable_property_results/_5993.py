"""ResultsForOrderIncludingGroups"""

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
    _5992,
)

_RESULTS_FOR_ORDER_INCLUDING_GROUPS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForOrderIncludingGroups",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _5984,
    )

    Self = TypeVar("Self", bound="ResultsForOrderIncludingGroups")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForOrderIncludingGroups._Cast_ResultsForOrderIncludingGroups",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForOrderIncludingGroups",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForOrderIncludingGroups:
    """Special nested class for casting ResultsForOrderIncludingGroups to subclasses."""

    __parent__: "ResultsForOrderIncludingGroups"

    @property
    def results_for_order(self: "CastSelf") -> "_5992.ResultsForOrder":
        return self.__parent__._cast(_5992.ResultsForOrder)

    @property
    def results_for_order_including_groups(
        self: "CastSelf",
    ) -> "ResultsForOrderIncludingGroups":
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
class ResultsForOrderIncludingGroups(_5992.ResultsForOrder):
    """ResultsForOrderIncludingGroups

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_ORDER_INCLUDING_GROUPS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def groups(
        self: "Self",
    ) -> "List[_5984.HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Groups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ResultsForOrderIncludingGroups":
        """Cast to another type.

        Returns:
            _Cast_ResultsForOrderIncludingGroups
        """
        return _Cast_ResultsForOrderIncludingGroups(self)
