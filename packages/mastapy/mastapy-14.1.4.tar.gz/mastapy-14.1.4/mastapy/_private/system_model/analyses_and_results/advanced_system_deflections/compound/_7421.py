"""KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7415,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2723
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7288,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7347,
        _7381,
        _7407,
        _7419,
        _7420,
        _7428,
        _7447,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7702,
        _7705,
    )
    from mastapy._private.system_model.part_model.gears import _2610

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: (
        "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection"
    )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7415.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7415.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7381.ConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7381,
        )

        return self.__parent__._cast(
            _7381.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7407.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7407,
        )

        return self.__parent__._cast(_7407.GearSetCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7447.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7447,
        )

        return self.__parent__._cast(
            _7447.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7347.AbstractAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7347,
        )

        return self.__parent__._cast(
            _7347.AbstractAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7428.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7428,
        )

        return self.__parent__._cast(_7428.PartCompoundAdvancedSystemDeflection)

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
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
class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection(
    _7415.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
):
    """KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(
        self: "Self",
    ) -> "_2610.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(
        self: "Self",
    ) -> "_2610.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> (
        "List[_7288.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]"
    ):
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7419.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidSpiralBevelGearsCompoundAdvancedSystemDeflection",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7420.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidSpiralBevelMeshesCompoundAdvancedSystemDeflection",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> (
        "List[_7288.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]"
    ):
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection(
            self
        )
