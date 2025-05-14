"""DesignStateOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5783
from mastapy._private.utility_gui import _1908

_DESIGN_STATE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "DesignStateOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2270

    Self = TypeVar("Self", bound="DesignStateOptions")
    CastSelf = TypeVar("CastSelf", bound="DesignStateOptions._Cast_DesignStateOptions")


__docformat__ = "restructuredtext en"
__all__ = ("DesignStateOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignStateOptions:
    """Special nested class for casting DesignStateOptions to subclasses."""

    __parent__: "DesignStateOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_1908.ColumnInputOptions":
        return self.__parent__._cast(_1908.ColumnInputOptions)

    @property
    def design_state_options(self: "CastSelf") -> "DesignStateOptions":
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
class DesignStateOptions(_1908.ColumnInputOptions):
    """DesignStateOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_STATE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def create_new_design_state(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateNewDesignState")

        if temp is None:
            return False

        return temp

    @create_new_design_state.setter
    @enforce_parameter_types
    def create_new_design_state(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateNewDesignState",
            bool(value) if value is not None else False,
        )

    @property
    def design_state(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_DesignState":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]"""
        temp = pythonnet_property_get(self.wrapped, "DesignState")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DesignState",
        )(temp)

    @design_state.setter
    @enforce_parameter_types
    def design_state(self: "Self", value: "_5783.DesignState") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_DesignState.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "DesignState", value)

    @property
    def design_state_destinations(
        self: "Self",
    ) -> "List[_2270.DutyCycleImporterDesignEntityMatch[_5783.DesignState]]":
        """List[mastapy.system_model.DutyCycleImporterDesignEntityMatch[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStateDestinations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DesignStateOptions":
        """Cast to another type.

        Returns:
            _Cast_DesignStateOptions
        """
        return _Cast_DesignStateOptions(self)
