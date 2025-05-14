"""EntityVectorState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ENTITY_VECTOR_STATE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.States", "EntityVectorState"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1584
    from mastapy._private.nodal_analysis.states import _124, _125, _127, _128

    Self = TypeVar("Self", bound="EntityVectorState")
    CastSelf = TypeVar("CastSelf", bound="EntityVectorState._Cast_EntityVectorState")


__docformat__ = "restructuredtext en"
__all__ = ("EntityVectorState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EntityVectorState:
    """Special nested class for casting EntityVectorState to subclasses."""

    __parent__: "EntityVectorState"

    @property
    def element_scalar_state(self: "CastSelf") -> "_124.ElementScalarState":
        from mastapy._private.nodal_analysis.states import _124

        return self.__parent__._cast(_124.ElementScalarState)

    @property
    def element_vector_state(self: "CastSelf") -> "_125.ElementVectorState":
        from mastapy._private.nodal_analysis.states import _125

        return self.__parent__._cast(_125.ElementVectorState)

    @property
    def node_scalar_state(self: "CastSelf") -> "_127.NodeScalarState":
        from mastapy._private.nodal_analysis.states import _127

        return self.__parent__._cast(_127.NodeScalarState)

    @property
    def node_vector_state(self: "CastSelf") -> "_128.NodeVectorState":
        from mastapy._private.nodal_analysis.states import _128

        return self.__parent__._cast(_128.NodeVectorState)

    @property
    def entity_vector_state(self: "CastSelf") -> "EntityVectorState":
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
class EntityVectorState(_0.APIBase):
    """EntityVectorState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ENTITY_VECTOR_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def degrees_of_freedom_per_entity(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreesOfFreedomPerEntity")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_entities(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfEntities")

        if temp is None:
            return 0

        return temp

    @property
    def vector(self: "Self") -> "_1584.RealVector":
        """mastapy.math_utility.RealVector

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Vector")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_EntityVectorState":
        """Cast to another type.

        Returns:
            _Cast_EntityVectorState
        """
        return _Cast_EntityVectorState(self)
