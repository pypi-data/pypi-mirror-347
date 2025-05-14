"""ConceptGearMesh"""

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
from mastapy._private.system_model.connections_and_sockets.gears import _2376

_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.concept import _1225
    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.connections_and_sockets import _2335, _2344

    Self = TypeVar("Self", bound="ConceptGearMesh")
    CastSelf = TypeVar("CastSelf", bound="ConceptGearMesh._Cast_ConceptGearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearMesh:
    """Special nested class for casting ConceptGearMesh to subclasses."""

    __parent__: "ConceptGearMesh"

    @property
    def gear_mesh(self: "CastSelf") -> "_2376.GearMesh":
        return self.__parent__._cast(_2376.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2344.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2344

        return self.__parent__._cast(_2344.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2335.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "ConceptGearMesh":
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
class ConceptGearMesh(_2376.GearMesh):
    """ConceptGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def pinion_drop_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionDropAngle")

        if temp is None:
            return 0.0

        return temp

    @pinion_drop_angle.setter
    @enforce_parameter_types
    def pinion_drop_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionDropAngle", float(value) if value is not None else 0.0
        )

    @property
    def wheel_drop_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelDropAngle")

        if temp is None:
            return 0.0

        return temp

    @wheel_drop_angle.setter
    @enforce_parameter_types
    def wheel_drop_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelDropAngle", float(value) if value is not None else 0.0
        )

    @property
    def active_gear_mesh_design(self: "Self") -> "_1225.ConceptGearMeshDesign":
        """mastapy.gears.gear_designs.concept.ConceptGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def concept_gear_mesh_design(self: "Self") -> "_1225.ConceptGearMeshDesign":
        """mastapy.gears.gear_designs.concept.ConceptGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearMesh":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearMesh
        """
        return _Cast_ConceptGearMesh(self)
