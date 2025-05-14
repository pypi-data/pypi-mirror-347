"""DynamicForceResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.harmonic_load_data import _1436

_DYNAMIC_FORCE_RESULTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "DynamicForceResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1438, _1442
    from mastapy._private.math_utility import _1571

    Self = TypeVar("Self", bound="DynamicForceResults")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicForceResults._Cast_DynamicForceResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicForceResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicForceResults:
    """Special nested class for casting DynamicForceResults to subclasses."""

    __parent__: "DynamicForceResults"

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1436.ElectricMachineHarmonicLoadDataBase":
        return self.__parent__._cast(_1436.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1442.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1442

        return self.__parent__._cast(_1442.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1438.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1438

        return self.__parent__._cast(_1438.HarmonicLoadDataBase)

    @property
    def dynamic_force_results(self: "CastSelf") -> "DynamicForceResults":
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
class DynamicForceResults(_1436.ElectricMachineHarmonicLoadDataBase):
    """DynamicForceResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_FORCE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitations(self: "Self") -> "List[_1571.FourierSeries]":
        """List[mastapy.math_utility.FourierSeries]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Excitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicForceResults":
        """Cast to another type.

        Returns:
            _Cast_DynamicForceResults
        """
        return _Cast_DynamicForceResults(self)
