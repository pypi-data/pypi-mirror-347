"""BasicConicalGearMachineSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BASIC_CONICAL_GEAR_MACHINE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.BasicMachineSettings",
    "BasicConicalGearMachineSettings",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import (
        _853,
        _854,
    )

    Self = TypeVar("Self", bound="BasicConicalGearMachineSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BasicConicalGearMachineSettings._Cast_BasicConicalGearMachineSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicConicalGearMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BasicConicalGearMachineSettings:
    """Special nested class for casting BasicConicalGearMachineSettings to subclasses."""

    __parent__: "BasicConicalGearMachineSettings"

    @property
    def basic_conical_gear_machine_settings_formate(
        self: "CastSelf",
    ) -> "_853.BasicConicalGearMachineSettingsFormate":
        from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import (
            _853,
        )

        return self.__parent__._cast(_853.BasicConicalGearMachineSettingsFormate)

    @property
    def basic_conical_gear_machine_settings_generated(
        self: "CastSelf",
    ) -> "_854.BasicConicalGearMachineSettingsGenerated":
        from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import (
            _854,
        )

        return self.__parent__._cast(_854.BasicConicalGearMachineSettingsGenerated)

    @property
    def basic_conical_gear_machine_settings(
        self: "CastSelf",
    ) -> "BasicConicalGearMachineSettings":
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
class BasicConicalGearMachineSettings(_0.APIBase):
    """BasicConicalGearMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BASIC_CONICAL_GEAR_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def machine_centre_to_back(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MachineCentreToBack")

        if temp is None:
            return 0.0

        return temp

    @machine_centre_to_back.setter
    @enforce_parameter_types
    def machine_centre_to_back(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MachineCentreToBack",
            float(value) if value is not None else 0.0,
        )

    @property
    def machine_root_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MachineRootAngle")

        if temp is None:
            return 0.0

        return temp

    @machine_root_angle.setter
    @enforce_parameter_types
    def machine_root_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MachineRootAngle", float(value) if value is not None else 0.0
        )

    @property
    def sliding_base(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SlidingBase")

        if temp is None:
            return 0.0

        return temp

    @sliding_base.setter
    @enforce_parameter_types
    def sliding_base(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SlidingBase", float(value) if value is not None else 0.0
        )

    @property
    def swivel_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SwivelAngle")

        if temp is None:
            return 0.0

        return temp

    @swivel_angle.setter
    @enforce_parameter_types
    def swivel_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SwivelAngle", float(value) if value is not None else 0.0
        )

    @property
    def tilt_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltAngle")

        if temp is None:
            return 0.0

        return temp

    @tilt_angle.setter
    @enforce_parameter_types
    def tilt_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BasicConicalGearMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_BasicConicalGearMachineSettings
        """
        return _Cast_BasicConicalGearMachineSettings(self)
