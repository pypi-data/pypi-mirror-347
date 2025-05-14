"""OptimizationStrategyBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _1890

_OPTIMIZATION_STRATEGY_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "OptimizationStrategyBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.optimization import _2289, _2292, _2297

    Self = TypeVar("Self", bound="OptimizationStrategyBase")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimizationStrategyBase._Cast_OptimizationStrategyBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationStrategyBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationStrategyBase:
    """Special nested class for casting OptimizationStrategyBase to subclasses."""

    __parent__: "OptimizationStrategyBase"

    @property
    def named_database_item(self: "CastSelf") -> "_1890.NamedDatabaseItem":
        return self.__parent__._cast(_1890.NamedDatabaseItem)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2289.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2289

        return self.__parent__._cast(_2289.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2292.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2292

        return self.__parent__._cast(_2292.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "_2297.OptimizationStrategy":
        from mastapy._private.system_model.optimization import _2297

        return self.__parent__._cast(_2297.OptimizationStrategy)

    @property
    def optimization_strategy_base(self: "CastSelf") -> "OptimizationStrategyBase":
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
class OptimizationStrategyBase(_1890.NamedDatabaseItem):
    """OptimizationStrategyBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_STRATEGY_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationStrategyBase":
        """Cast to another type.

        Returns:
            _Cast_OptimizationStrategyBase
        """
        return _Cast_OptimizationStrategyBase(self)
