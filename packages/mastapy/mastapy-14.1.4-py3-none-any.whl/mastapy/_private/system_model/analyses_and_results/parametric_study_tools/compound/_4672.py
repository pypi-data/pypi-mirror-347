"""ZerolBevelGearSetCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4560,
)

_ZEROL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ZerolBevelGearSetCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2723
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7702,
        _7705,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4541,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4542,
        _4548,
        _4576,
        _4602,
        _4623,
        _4642,
        _4670,
        _4671,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7676
    from mastapy._private.system_model.part_model.gears import _2623

    Self = TypeVar("Self", bound="ZerolBevelGearSetCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearSetCompoundParametricStudyTool._Cast_ZerolBevelGearSetCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSetCompoundParametricStudyTool:
    """Special nested class for casting ZerolBevelGearSetCompoundParametricStudyTool to subclasses."""

    __parent__: "ZerolBevelGearSetCompoundParametricStudyTool"

    @property
    def bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4560.BevelGearSetCompoundParametricStudyTool":
        return self.__parent__._cast(_4560.BevelGearSetCompoundParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4548.AGMAGleasonConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4548,
        )

        return self.__parent__._cast(
            _4548.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        )

    @property
    def conical_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4576.ConicalGearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4576,
        )

        return self.__parent__._cast(_4576.ConicalGearSetCompoundParametricStudyTool)

    @property
    def gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4602.GearSetCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4602,
        )

        return self.__parent__._cast(_4602.GearSetCompoundParametricStudyTool)

    @property
    def specialised_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4642.SpecialisedAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4642,
        )

        return self.__parent__._cast(
            _4642.SpecialisedAssemblyCompoundParametricStudyTool
        )

    @property
    def abstract_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4542.AbstractAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4542,
        )

        return self.__parent__._cast(_4542.AbstractAssemblyCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4623.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4623,
        )

        return self.__parent__._cast(_4623.PartCompoundParametricStudyTool)

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
    def zerol_bevel_gear_set_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ZerolBevelGearSetCompoundParametricStudyTool":
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
class ZerolBevelGearSetCompoundParametricStudyTool(
    _4560.BevelGearSetCompoundParametricStudyTool
):
    """ZerolBevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2623.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2623.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7676.ZerolBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4541.ZerolBevelGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool]

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
    def zerol_bevel_gears_compound_parametric_study_tool(
        self: "Self",
    ) -> "List[_4670.ZerolBevelGearCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearCompoundParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelGearsCompoundParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes_compound_parametric_study_tool(
        self: "Self",
    ) -> "List[_4671.ZerolBevelGearMeshCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearMeshCompoundParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelMeshesCompoundParametricStudyTool"
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
    ) -> "List[_4541.ZerolBevelGearSetParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearSetCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSetCompoundParametricStudyTool
        """
        return _Cast_ZerolBevelGearSetCompoundParametricStudyTool(self)
