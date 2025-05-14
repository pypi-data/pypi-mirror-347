"""ShaftDamageResultsTableAndChart"""

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
from mastapy._private.utility.report import _1815

_SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftDamageResultsTableAndChart"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.enums import _1881
    from mastapy._private.utility.report import _1822, _1828, _1829, _1830

    Self = TypeVar("Self", bound="ShaftDamageResultsTableAndChart")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDamageResultsTableAndChart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftDamageResultsTableAndChart:
    """Special nested class for casting ShaftDamageResultsTableAndChart to subclasses."""

    __parent__: "ShaftDamageResultsTableAndChart"

    @property
    def custom_report_chart(self: "CastSelf") -> "_1815.CustomReportChart":
        return self.__parent__._cast(_1815.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1828.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1828

        return self.__parent__._cast(_1828.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1829.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1829

        return self.__parent__._cast(_1829.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1830.CustomReportNameableItem":
        from mastapy._private.utility.report import _1830

        return self.__parent__._cast(_1830.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1822.CustomReportItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportItem)

    @property
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "ShaftDamageResultsTableAndChart":
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
class ShaftDamageResultsTableAndChart(_1815.CustomReportChart):
    """ShaftDamageResultsTableAndChart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def display(self: "Self") -> "_1881.TableAndChartOptions":
        """mastapy.utility.enums.TableAndChartOptions"""
        temp = pythonnet_property_get(self.wrapped, "Display")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.enums._1881", "TableAndChartOptions"
        )(value)

    @display.setter
    @enforce_parameter_types
    def display(self: "Self", value: "_1881.TableAndChartOptions") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )
        pythonnet_property_set(self.wrapped, "Display", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftDamageResultsTableAndChart":
        """Cast to another type.

        Returns:
            _Cast_ShaftDamageResultsTableAndChart
        """
        return _Cast_ShaftDamageResultsTableAndChart(self)
