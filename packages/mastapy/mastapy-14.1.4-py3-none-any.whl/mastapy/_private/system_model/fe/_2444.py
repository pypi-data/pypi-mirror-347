"""FEPartWithBatchOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_PART_WITH_BATCH_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FEPartWithBatchOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private.system_model.fe import _2453

    Self = TypeVar("Self", bound="FEPartWithBatchOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="FEPartWithBatchOptions._Cast_FEPartWithBatchOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartWithBatchOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartWithBatchOptions:
    """Special nested class for casting FEPartWithBatchOptions to subclasses."""

    __parent__: "FEPartWithBatchOptions"

    @property
    def fe_part_with_batch_options(self: "CastSelf") -> "FEPartWithBatchOptions":
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
class FEPartWithBatchOptions(_0.APIBase):
    """FEPartWithBatchOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_WITH_BATCH_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def all_selected(self: "Self") -> "Optional[bool]":
        """Optional[bool]"""
        temp = pythonnet_property_get(self.wrapped, "AllSelected")

        if temp is None:
            return None

        return temp

    @all_selected.setter
    @enforce_parameter_types
    def all_selected(self: "Self", value: "Optional[bool]") -> None:
        pythonnet_property_set(self.wrapped, "AllSelected", value)

    @property
    def fe_part(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEPart")

        if temp is None:
            return ""

        return temp

    @property
    def f_es(self: "Self") -> "List[_2453.FESubstructureWithBatchOptions]":
        """List[mastapy.system_model.fe.FESubstructureWithBatchOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def f_es_with_external_files(
        self: "Self",
    ) -> "List[_2453.FESubstructureWithBatchOptions]":
        """List[mastapy.system_model.fe.FESubstructureWithBatchOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEsWithExternalFiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartWithBatchOptions":
        """Cast to another type.

        Returns:
            _Cast_FEPartWithBatchOptions
        """
        return _Cast_FEPartWithBatchOptions(self)
