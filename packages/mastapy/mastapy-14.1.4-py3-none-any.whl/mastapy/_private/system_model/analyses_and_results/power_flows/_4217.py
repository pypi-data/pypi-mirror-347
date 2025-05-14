"""PowerFlowDrawStyle"""

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
from mastapy._private.geometry import _325

_POWER_FLOW_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PowerFlowDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _326
    from mastapy._private.system_model.analyses_and_results.power_flows import _4171

    Self = TypeVar("Self", bound="PowerFlowDrawStyle")
    CastSelf = TypeVar("CastSelf", bound="PowerFlowDrawStyle._Cast_PowerFlowDrawStyle")


__docformat__ = "restructuredtext en"
__all__ = ("PowerFlowDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerFlowDrawStyle:
    """Special nested class for casting PowerFlowDrawStyle to subclasses."""

    __parent__: "PowerFlowDrawStyle"

    @property
    def draw_style(self: "CastSelf") -> "_325.DrawStyle":
        return self.__parent__._cast(_325.DrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_326.DrawStyleBase":
        from mastapy._private.geometry import _326

        return self.__parent__._cast(_326.DrawStyleBase)

    @property
    def cylindrical_gear_geometric_entity_draw_style(
        self: "CastSelf",
    ) -> "_4171.CylindricalGearGeometricEntityDrawStyle":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4171

        return self.__parent__._cast(_4171.CylindricalGearGeometricEntityDrawStyle)

    @property
    def power_flow_draw_style(self: "CastSelf") -> "PowerFlowDrawStyle":
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
class PowerFlowDrawStyle(_325.DrawStyle):
    """PowerFlowDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_FLOW_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def colour_loaded_flanks(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ColourLoadedFlanks")

        if temp is None:
            return False

        return temp

    @colour_loaded_flanks.setter
    @enforce_parameter_types
    def colour_loaded_flanks(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ColourLoadedFlanks",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PowerFlowDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_PowerFlowDrawStyle
        """
        return _Cast_PowerFlowDrawStyle(self)
