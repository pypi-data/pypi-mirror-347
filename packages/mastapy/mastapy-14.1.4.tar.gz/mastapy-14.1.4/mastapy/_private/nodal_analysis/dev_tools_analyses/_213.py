"""FENodeSelectionDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, overridable_enum_runtime, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item_and_image
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.dev_tools_analyses import _214

_FE_NODE_SELECTION_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FENodeSelectionDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="FENodeSelectionDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="FENodeSelectionDrawStyle._Cast_FENodeSelectionDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FENodeSelectionDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FENodeSelectionDrawStyle:
    """Special nested class for casting FENodeSelectionDrawStyle to subclasses."""

    __parent__: "FENodeSelectionDrawStyle"

    @property
    def fe_node_selection_draw_style(self: "CastSelf") -> "FENodeSelectionDrawStyle":
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
class FENodeSelectionDrawStyle(_0.APIBase):
    """FENodeSelectionDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_NODE_SELECTION_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def add_to_selection(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AddToSelection")

        if temp is None:
            return False

        return temp

    @add_to_selection.setter
    @enforce_parameter_types
    def add_to_selection(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "AddToSelection", bool(value) if value is not None else False
        )

    @property
    def region_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RegionSize")

        if temp is None:
            return 0.0

        return temp

    @region_size.setter
    @enforce_parameter_types
    def region_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RegionSize", float(value) if value is not None else 0.0
        )

    @property
    def selection_mode(
        self: "Self",
    ) -> (
        "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode"
    ):
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.FESelectionMode]"""
        temp = pythonnet_property_get(self.wrapped, "SelectionMode")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @selection_mode.setter
    @enforce_parameter_types
    def selection_mode(self: "Self", value: "_214.FESelectionMode") -> None:
        wrapper_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode.wrapper_type()
        enclosed_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESelectionMode.implicit_type()
        value = wrapper_type[enclosed_type](value if value is not None else None)
        pythonnet_property_set(self.wrapped, "SelectionMode", value)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def clear_selection(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearSelection")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_FENodeSelectionDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FENodeSelectionDrawStyle
        """
        return _Cast_FENodeSelectionDrawStyle(self)
