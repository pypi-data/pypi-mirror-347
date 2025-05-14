"""RigidlyConnectedComponentGroupSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2724

_RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "RigidlyConnectedComponentGroupSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1576
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2787,
    )

    Self = TypeVar("Self", bound="RigidlyConnectedComponentGroupSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidlyConnectedComponentGroupSystemDeflection._Cast_RigidlyConnectedComponentGroupSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidlyConnectedComponentGroupSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidlyConnectedComponentGroupSystemDeflection:
    """Special nested class for casting RigidlyConnectedComponentGroupSystemDeflection to subclasses."""

    __parent__: "RigidlyConnectedComponentGroupSystemDeflection"

    @property
    def design_entity_group_analysis(
        self: "CastSelf",
    ) -> "_2724.DesignEntityGroupAnalysis":
        return self.__parent__._cast(_2724.DesignEntityGroupAnalysis)

    @property
    def rigidly_connected_component_group_system_deflection(
        self: "CastSelf",
    ) -> "RigidlyConnectedComponentGroupSystemDeflection":
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
class RigidlyConnectedComponentGroupSystemDeflection(_2724.DesignEntityGroupAnalysis):
    """RigidlyConnectedComponentGroupSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mass_properties(self: "Self") -> "_1576.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def components(self: "Self") -> "List[_2787.ComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Components")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RigidlyConnectedComponentGroupSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_RigidlyConnectedComponentGroupSystemDeflection
        """
        return _Cast_RigidlyConnectedComponentGroupSystemDeflection(self)
