"""HarmonicLoadDataImportFromMotorPackages"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1440
from mastapy._private.system_model.analyses_and_results.static_loads import _7587

_HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "HarmonicLoadDataImportFromMotorPackages",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7566,
        _7584,
        _7586,
        _7589,
        _7590,
    )

    Self = TypeVar("Self", bound="HarmonicLoadDataImportFromMotorPackages")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicLoadDataImportFromMotorPackages._Cast_HarmonicLoadDataImportFromMotorPackages",
    )

T = TypeVar("T", bound="_7566.ElectricMachineHarmonicLoadImportOptionsBase")

__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataImportFromMotorPackages",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataImportFromMotorPackages:
    """Special nested class for casting HarmonicLoadDataImportFromMotorPackages to subclasses."""

    __parent__: "HarmonicLoadDataImportFromMotorPackages"

    @property
    def harmonic_load_data_import_base(
        self: "CastSelf",
    ) -> "_7587.HarmonicLoadDataImportBase":
        return self.__parent__._cast(_7587.HarmonicLoadDataImportBase)

    @property
    def harmonic_load_data_csv_import(
        self: "CastSelf",
    ) -> "_7584.HarmonicLoadDataCSVImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7584,
        )

        return self.__parent__._cast(_7584.HarmonicLoadDataCSVImport)

    @property
    def harmonic_load_data_flux_import(
        self: "CastSelf",
    ) -> "_7586.HarmonicLoadDataFluxImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7586,
        )

        return self.__parent__._cast(_7586.HarmonicLoadDataFluxImport)

    @property
    def harmonic_load_data_jmag_import(
        self: "CastSelf",
    ) -> "_7589.HarmonicLoadDataJMAGImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7589,
        )

        return self.__parent__._cast(_7589.HarmonicLoadDataJMAGImport)

    @property
    def harmonic_load_data_motor_cad_import(
        self: "CastSelf",
    ) -> "_7590.HarmonicLoadDataMotorCADImport":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7590,
        )

        return self.__parent__._cast(_7590.HarmonicLoadDataMotorCADImport)

    @property
    def harmonic_load_data_import_from_motor_packages(
        self: "CastSelf",
    ) -> "HarmonicLoadDataImportFromMotorPackages":
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
class HarmonicLoadDataImportFromMotorPackages(_7587.HarmonicLoadDataImportBase[T]):
    """HarmonicLoadDataImportFromMotorPackages

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_slice_number(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "AxialSliceNumber")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @axial_slice_number.setter
    @enforce_parameter_types
    def axial_slice_number(self: "Self", value: "int") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0
        )
        pythonnet_property_set(self.wrapped, "AxialSliceNumber", value)

    @property
    def data_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(self.wrapped, "DataType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type.setter
    @enforce_parameter_types
    def data_type(self: "Self", value: "_1440.HarmonicLoadDataType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DataType", value)

    @property
    def speed(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_float":
        """ListWithSelectedItem[float]"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_float",
        )(temp)

    @speed.setter
    @enforce_parameter_types
    def speed(self: "Self", value: "float") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_float.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0
        )
        pythonnet_property_set(self.wrapped, "Speed", value)

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataImportFromMotorPackages":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataImportFromMotorPackages
        """
        return _Cast_HarmonicLoadDataImportFromMotorPackages(self)
