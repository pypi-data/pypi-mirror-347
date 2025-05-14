"""CADElectricMachineDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.electric_machines import _1312

_CAD_ELECTRIC_MACHINE_DETAIL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CADElectricMachineDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1299, _1300
    from mastapy._private.nodal_analysis.geometry_modeller_link import _169

    Self = TypeVar("Self", bound="CADElectricMachineDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="CADElectricMachineDetail._Cast_CADElectricMachineDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CADElectricMachineDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADElectricMachineDetail:
    """Special nested class for casting CADElectricMachineDetail to subclasses."""

    __parent__: "CADElectricMachineDetail"

    @property
    def electric_machine_detail(self: "CastSelf") -> "_1312.ElectricMachineDetail":
        return self.__parent__._cast(_1312.ElectricMachineDetail)

    @property
    def cad_electric_machine_detail(self: "CastSelf") -> "CADElectricMachineDetail":
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
class CADElectricMachineDetail(_1312.ElectricMachineDetail):
    """CADElectricMachineDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_ELECTRIC_MACHINE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def geometry_modeller_dimensions(self: "Self") -> "_169.GeometryModellerDimensions":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimensions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDimensions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rotor(self: "Self") -> "_1299.CADRotor":
        """mastapy.electric_machines.CADRotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stator(self: "Self") -> "_1300.CADStator":
        """mastapy.electric_machines.CADStator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def embed_geometry_modeller_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "EmbedGeometryModellerFile")

    def open_embedded_geometry_modeller_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "OpenEmbeddedGeometryModellerFile")

    def reread_geometry_from_geometry_modeller(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RereadGeometryFromGeometryModeller")

    @property
    def cast_to(self: "Self") -> "_Cast_CADElectricMachineDetail":
        """Cast to another type.

        Returns:
            _Cast_CADElectricMachineDetail
        """
        return _Cast_CADElectricMachineDetail(self)
