"""WormGrinderSimulationCalculator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _774

_WORM_GRINDER_SIMULATION_CALCULATOR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "WormGrinderSimulationCalculator",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _762
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _759

    Self = TypeVar("Self", bound="WormGrinderSimulationCalculator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrinderSimulationCalculator._Cast_WormGrinderSimulationCalculator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrinderSimulationCalculator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrinderSimulationCalculator:
    """Special nested class for casting WormGrinderSimulationCalculator to subclasses."""

    __parent__: "WormGrinderSimulationCalculator"

    @property
    def rack_simulation_calculator(self: "CastSelf") -> "_774.RackSimulationCalculator":
        return self.__parent__._cast(_774.RackSimulationCalculator)

    @property
    def cutter_simulation_calc(self: "CastSelf") -> "_762.CutterSimulationCalc":
        from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
            _762,
        )

        return self.__parent__._cast(_762.CutterSimulationCalc)

    @property
    def worm_grinder_simulation_calculator(
        self: "CastSelf",
    ) -> "WormGrinderSimulationCalculator":
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
class WormGrinderSimulationCalculator(_774.RackSimulationCalculator):
    """WormGrinderSimulationCalculator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDER_SIMULATION_CALCULATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def worm_grinder(self: "Self") -> "_759.CylindricalGearWormGrinderShape":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CylindricalGearWormGrinderShape

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGrinder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrinderSimulationCalculator":
        """Cast to another type.

        Returns:
            _Cast_WormGrinderSimulationCalculator
        """
        return _Cast_WormGrinderSimulationCalculator(self)
