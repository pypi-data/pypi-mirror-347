"""OilSealCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2961,
)

_OIL_SEAL_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "OilSealCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2723
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7702,
        _7705,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2858,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2950,
        _3005,
        _3007,
    )
    from mastapy._private.system_model.part_model import _2532

    Self = TypeVar("Self", bound="OilSealCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OilSealCompoundSystemDeflection._Cast_OilSealCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OilSealCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilSealCompoundSystemDeflection:
    """Special nested class for casting OilSealCompoundSystemDeflection to subclasses."""

    __parent__: "OilSealCompoundSystemDeflection"

    @property
    def connector_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2961.ConnectorCompoundSystemDeflection":
        return self.__parent__._cast(_2961.ConnectorCompoundSystemDeflection)

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3005.MountableComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3005,
        )

        return self.__parent__._cast(_3005.MountableComponentCompoundSystemDeflection)

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2950.ComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2950,
        )

        return self.__parent__._cast(_2950.ComponentCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3007.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3007,
        )

        return self.__parent__._cast(_3007.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7705.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7705,
        )

        return self.__parent__._cast(_7705.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7702.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7702,
        )

        return self.__parent__._cast(_7702.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2723.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2723

        return self.__parent__._cast(_2723.DesignEntityAnalysis)

    @property
    def oil_seal_compound_system_deflection(
        self: "CastSelf",
    ) -> "OilSealCompoundSystemDeflection":
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
class OilSealCompoundSystemDeflection(_2961.ConnectorCompoundSystemDeflection):
    """OilSealCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_SEAL_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def reliability_for_oil_seal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityForOilSeal")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2532.OilSeal":
        """mastapy.system_model.part_model.OilSeal

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2858.OilSealSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.OilSealSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(self: "Self") -> "List[_2858.OilSealSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.OilSealSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_OilSealCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_OilSealCompoundSystemDeflection
        """
        return _Cast_OilSealCompoundSystemDeflection(self)
