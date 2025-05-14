"""CVTPulleyLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7628

_CVT_PULLEY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CVTPulleyLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2723, _2725, _2729
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7523,
        _7538,
        _7612,
        _7616,
    )
    from mastapy._private.system_model.part_model.couplings import _2658

    Self = TypeVar("Self", bound="CVTPulleyLoadCase")
    CastSelf = TypeVar("CastSelf", bound="CVTPulleyLoadCase._Cast_CVTPulleyLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyLoadCase:
    """Special nested class for casting CVTPulleyLoadCase to subclasses."""

    __parent__: "CVTPulleyLoadCase"

    @property
    def pulley_load_case(self: "CastSelf") -> "_7628.PulleyLoadCase":
        return self.__parent__._cast(_7628.PulleyLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7538.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7538,
        )

        return self.__parent__._cast(_7538.CouplingHalfLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7612.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7612,
        )

        return self.__parent__._cast(_7612.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7523.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7523,
        )

        return self.__parent__._cast(_7523.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7616.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7616,
        )

        return self.__parent__._cast(_7616.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2729.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2729

        return self.__parent__._cast(_2729.PartAnalysis)

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
    def cvt_pulley_load_case(self: "CastSelf") -> "CVTPulleyLoadCase":
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
class CVTPulleyLoadCase(_7628.PulleyLoadCase):
    """CVTPulleyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_PULLEY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def clamping_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClampingForce")

        if temp is None:
            return 0.0

        return temp

    @clamping_force.setter
    @enforce_parameter_types
    def clamping_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClampingForce", float(value) if value is not None else 0.0
        )

    @property
    def effective_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_nodes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfNodes")

        if temp is None:
            return 0

        return temp

    @number_of_nodes.setter
    @enforce_parameter_types
    def number_of_nodes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfNodes", int(value) if value is not None else 0
        )

    @property
    def component_design(self: "Self") -> "_2658.CVTPulley":
        """mastapy.system_model.part_model.couplings.CVTPulley

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTPulleyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyLoadCase
        """
        return _Cast_CVTPulleyLoadCase(self)
