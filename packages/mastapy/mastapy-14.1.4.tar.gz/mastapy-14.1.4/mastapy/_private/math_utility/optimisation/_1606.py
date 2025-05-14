"""ParetoOptimisationStrategy"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.utility.databases import _1890

_PARETO_OPTIMISATION_STRATEGY = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationStrategy"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1604, _1605, _1608

    Self = TypeVar("Self", bound="ParetoOptimisationStrategy")
    CastSelf = TypeVar(
        "CastSelf", bound="ParetoOptimisationStrategy._Cast_ParetoOptimisationStrategy"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationStrategy",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationStrategy:
    """Special nested class for casting ParetoOptimisationStrategy to subclasses."""

    __parent__: "ParetoOptimisationStrategy"

    @property
    def named_database_item(self: "CastSelf") -> "_1890.NamedDatabaseItem":
        return self.__parent__._cast(_1890.NamedDatabaseItem)

    @property
    def pareto_optimisation_strategy(self: "CastSelf") -> "ParetoOptimisationStrategy":
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
class ParetoOptimisationStrategy(_1890.NamedDatabaseItem):
    """ParetoOptimisationStrategy

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_STRATEGY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def charts(
        self: "Self",
    ) -> "List[_1608.ParetoOptimisationStrategyChartInformation]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationStrategyChartInformation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Charts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def inputs(self: "Self") -> "List[_1604.ParetoOptimisationInput]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationInput]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Inputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def outputs(self: "Self") -> "List[_1605.ParetoOptimisationOutput]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationOutput]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Outputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddChart")

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationStrategy":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationStrategy
        """
        return _Cast_ParetoOptimisationStrategy(self)
