"""BevelGearISOMaterial"""

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
from mastapy._private.gears.materials import _607

_BEVEL_GEAR_ISO_MATERIAL = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "BevelGearISOMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _616
    from mastapy._private.materials import _288, _297
    from mastapy._private.utility.databases import _1890

    Self = TypeVar("Self", bound="BevelGearISOMaterial")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelGearISOMaterial._Cast_BevelGearISOMaterial"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearISOMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearISOMaterial:
    """Special nested class for casting BevelGearISOMaterial to subclasses."""

    __parent__: "BevelGearISOMaterial"

    @property
    def bevel_gear_material(self: "CastSelf") -> "_607.BevelGearMaterial":
        return self.__parent__._cast(_607.BevelGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_616.GearMaterial":
        from mastapy._private.gears.materials import _616

        return self.__parent__._cast(_616.GearMaterial)

    @property
    def material(self: "CastSelf") -> "_288.Material":
        from mastapy._private.materials import _288

        return self.__parent__._cast(_288.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_1890.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1890

        return self.__parent__._cast(_1890.NamedDatabaseItem)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "BevelGearISOMaterial":
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
class BevelGearISOMaterial(_607.BevelGearMaterial):
    """BevelGearISOMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_ISO_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_bending_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableBendingStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_bending_stress.setter
    @enforce_parameter_types
    def allowable_bending_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableBendingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def allowable_contact_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_contact_stress.setter
    @enforce_parameter_types
    def allowable_contact_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def iso_material_type(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ISOMaterialType")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @iso_material_type.setter
    @enforce_parameter_types
    def iso_material_type(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "ISOMaterialType", value)

    @property
    def limited_pitting_allowed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LimitedPittingAllowed")

        if temp is None:
            return False

        return temp

    @limited_pitting_allowed.setter
    @enforce_parameter_types
    def limited_pitting_allowed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitedPittingAllowed",
            bool(value) if value is not None else False,
        )

    @property
    def long_life_life_factor_bending(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LongLifeLifeFactorBending")

        if temp is None:
            return 0.0

        return temp

    @long_life_life_factor_bending.setter
    @enforce_parameter_types
    def long_life_life_factor_bending(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LongLifeLifeFactorBending",
            float(value) if value is not None else 0.0,
        )

    @property
    def long_life_life_factor_contact(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LongLifeLifeFactorContact")

        if temp is None:
            return 0.0

        return temp

    @long_life_life_factor_contact.setter
    @enforce_parameter_types
    def long_life_life_factor_contact(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LongLifeLifeFactorContact",
            float(value) if value is not None else 0.0,
        )

    @property
    def material_has_a_well_defined_yield_point(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "MaterialHasAWellDefinedYieldPoint")

        if temp is None:
            return False

        return temp

    @material_has_a_well_defined_yield_point.setter
    @enforce_parameter_types
    def material_has_a_well_defined_yield_point(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaterialHasAWellDefinedYieldPoint",
            bool(value) if value is not None else False,
        )

    @property
    def n0_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "N0Bending")

        if temp is None:
            return 0.0

        return temp

    @property
    def n0_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "N0Contact")

        if temp is None:
            return 0.0

        return temp

    @property
    def proof_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProofStress")

        if temp is None:
            return 0.0

        return temp

    @proof_stress.setter
    @enforce_parameter_types
    def proof_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ProofStress", float(value) if value is not None else 0.0
        )

    @property
    def quality_grade(self: "Self") -> "_297.QualityGrade":
        """mastapy.materials.QualityGrade"""
        temp = pythonnet_property_get(self.wrapped, "QualityGrade")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.QualityGrade")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._297", "QualityGrade"
        )(value)

    @quality_grade.setter
    @enforce_parameter_types
    def quality_grade(self: "Self", value: "_297.QualityGrade") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Materials.QualityGrade")
        pythonnet_property_set(self.wrapped, "QualityGrade", value)

    @property
    def specify_allowable_stress_numbers(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyAllowableStressNumbers")

        if temp is None:
            return False

        return temp

    @specify_allowable_stress_numbers.setter
    @enforce_parameter_types
    def specify_allowable_stress_numbers(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyAllowableStressNumbers",
            bool(value) if value is not None else False,
        )

    @property
    def use_iso633652003_material_definitions(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UseISO633652003MaterialDefinitions"
        )

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearISOMaterial":
        """Cast to another type.

        Returns:
            _Cast_BevelGearISOMaterial
        """
        return _Cast_BevelGearISOMaterial(self)
