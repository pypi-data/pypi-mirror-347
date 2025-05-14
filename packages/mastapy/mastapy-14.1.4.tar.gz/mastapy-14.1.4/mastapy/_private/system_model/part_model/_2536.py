"""PlanetCarrierSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1651

_PLANET_CARRIER_SETTINGS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrierSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2278
    from mastapy._private.utility import _1652

    Self = TypeVar("Self", bound="PlanetCarrierSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetCarrierSettings._Cast_PlanetCarrierSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetCarrierSettings:
    """Special nested class for casting PlanetCarrierSettings to subclasses."""

    __parent__: "PlanetCarrierSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1651.PerMachineSettings":
        return self.__parent__._cast(_1651.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1652.PersistentSingleton":
        from mastapy._private.utility import _1652

        return self.__parent__._cast(_1652.PersistentSingleton)

    @property
    def planet_carrier_settings(self: "CastSelf") -> "PlanetCarrierSettings":
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
class PlanetCarrierSettings(_1651.PerMachineSettings):
    """PlanetCarrierSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_CARRIER_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planet_pin_manufacturing_errors_coordinate_system(
        self: "Self",
    ) -> "_2278.PlanetPinManufacturingErrorsCoordinateSystem":
        """mastapy.system_model.PlanetPinManufacturingErrorsCoordinateSystem"""
        temp = pythonnet_property_get(
            self.wrapped, "PlanetPinManufacturingErrorsCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PlanetPinManufacturingErrorsCoordinateSystem",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2278",
            "PlanetPinManufacturingErrorsCoordinateSystem",
        )(value)

    @planet_pin_manufacturing_errors_coordinate_system.setter
    @enforce_parameter_types
    def planet_pin_manufacturing_errors_coordinate_system(
        self: "Self", value: "_2278.PlanetPinManufacturingErrorsCoordinateSystem"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PlanetPinManufacturingErrorsCoordinateSystem",
        )
        pythonnet_property_set(
            self.wrapped, "PlanetPinManufacturingErrorsCoordinateSystem", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetCarrierSettings":
        """Cast to another type.

        Returns:
            _Cast_PlanetCarrierSettings
        """
        return _Cast_PlanetCarrierSettings(self)
