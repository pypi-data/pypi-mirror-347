"""SpringDamperConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3888

_SPRING_DAMPER_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "SpringDamperConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2721, _2723, _2725
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7697,
        _7700,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3886,
        _3918,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7644
    from mastapy._private.system_model.connections_and_sockets.couplings import _2413

    Self = TypeVar("Self", bound="SpringDamperConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpringDamperConnectionStabilityAnalysis._Cast_SpringDamperConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperConnectionStabilityAnalysis:
    """Special nested class for casting SpringDamperConnectionStabilityAnalysis to subclasses."""

    __parent__: "SpringDamperConnectionStabilityAnalysis"

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3888.CouplingConnectionStabilityAnalysis":
        return self.__parent__._cast(_3888.CouplingConnectionStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3918.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3918,
        )

        return self.__parent__._cast(
            _3918.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3886.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3886,
        )

        return self.__parent__._cast(_3886.ConnectionStabilityAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7700.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7700,
        )

        return self.__parent__._cast(_7700.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7697.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7697,
        )

        return self.__parent__._cast(_7697.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2721.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2721

        return self.__parent__._cast(_2721.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2725.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2725

        return self.__parent__._cast(_2725.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2723.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2723

        return self.__parent__._cast(_2723.DesignEntityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "SpringDamperConnectionStabilityAnalysis":
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
class SpringDamperConnectionStabilityAnalysis(
    _3888.CouplingConnectionStabilityAnalysis
):
    """SpringDamperConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER_CONNECTION_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2413.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7644.SpringDamperConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamperConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperConnectionStabilityAnalysis
        """
        return _Cast_SpringDamperConnectionStabilityAnalysis(self)
