"""ComponentFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2563

_COMPONENT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ComponentFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2560,
        _2561,
        _2564,
        _2565,
        _2566,
        _2567,
        _2568,
        _2569,
        _2570,
        _2572,
        _2573,
        _2574,
        _2575,
        _2576,
        _2577,
    )

    Self = TypeVar("Self", bound="ComponentFromCAD")
    CastSelf = TypeVar("CastSelf", bound="ComponentFromCAD._Cast_ComponentFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentFromCAD:
    """Special nested class for casting ComponentFromCAD to subclasses."""

    __parent__: "ComponentFromCAD"

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2563.ComponentFromCADBase":
        return self.__parent__._cast(_2563.ComponentFromCADBase)

    @property
    def abstract_shaft_from_cad(self: "CastSelf") -> "_2560.AbstractShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2560

        return self.__parent__._cast(_2560.AbstractShaftFromCAD)

    @property
    def clutch_from_cad(self: "CastSelf") -> "_2561.ClutchFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2561

        return self.__parent__._cast(_2561.ClutchFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "_2564.ConceptBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2564

        return self.__parent__._cast(_2564.ConceptBearingFromCAD)

    @property
    def connector_from_cad(self: "CastSelf") -> "_2565.ConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2565

        return self.__parent__._cast(_2565.ConnectorFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2566.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2566

        return self.__parent__._cast(_2566.CylindricalGearFromCAD)

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2567.CylindricalGearInPlanetarySetFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2567

        return self.__parent__._cast(_2567.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "_2568.CylindricalPlanetGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2568

        return self.__parent__._cast(_2568.CylindricalPlanetGearFromCAD)

    @property
    def cylindrical_ring_gear_from_cad(
        self: "CastSelf",
    ) -> "_2569.CylindricalRingGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2569

        return self.__parent__._cast(_2569.CylindricalRingGearFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(
        self: "CastSelf",
    ) -> "_2570.CylindricalSunGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2570

        return self.__parent__._cast(_2570.CylindricalSunGearFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2572.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2572

        return self.__parent__._cast(_2572.MountableComponentFromCAD)

    @property
    def planet_shaft_from_cad(self: "CastSelf") -> "_2573.PlanetShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2573

        return self.__parent__._cast(_2573.PlanetShaftFromCAD)

    @property
    def pulley_from_cad(self: "CastSelf") -> "_2574.PulleyFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2574

        return self.__parent__._cast(_2574.PulleyFromCAD)

    @property
    def rigid_connector_from_cad(self: "CastSelf") -> "_2575.RigidConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2575

        return self.__parent__._cast(_2575.RigidConnectorFromCAD)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "_2576.RollingBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2576

        return self.__parent__._cast(_2576.RollingBearingFromCAD)

    @property
    def shaft_from_cad(self: "CastSelf") -> "_2577.ShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2577

        return self.__parent__._cast(_2577.ShaftFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "ComponentFromCAD":
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
class ComponentFromCAD(_2563.ComponentFromCADBase):
    """ComponentFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ComponentFromCAD
        """
        return _Cast_ComponentFromCAD(self)
