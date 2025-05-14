"""GearMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials import _288

_GEAR_MATERIAL = python_net_import("SMT.MastaAPI.Gears.Materials", "GearMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import (
        _602,
        _605,
        _607,
        _612,
        _624,
        _629,
        _633,
    )
    from mastapy._private.materials import _300
    from mastapy._private.utility.databases import _1890

    Self = TypeVar("Self", bound="GearMaterial")
    CastSelf = TypeVar("CastSelf", bound="GearMaterial._Cast_GearMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("GearMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMaterial:
    """Special nested class for casting GearMaterial to subclasses."""

    __parent__: "GearMaterial"

    @property
    def material(self: "CastSelf") -> "_288.Material":
        return self.__parent__._cast(_288.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_1890.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1890

        return self.__parent__._cast(_1890.NamedDatabaseItem)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_602.AGMACylindricalGearMaterial":
        from mastapy._private.gears.materials import _602

        return self.__parent__._cast(_602.AGMACylindricalGearMaterial)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_605.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _605

        return self.__parent__._cast(_605.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "_607.BevelGearMaterial":
        from mastapy._private.gears.materials import _607

        return self.__parent__._cast(_607.BevelGearMaterial)

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_612.CylindricalGearMaterial":
        from mastapy._private.gears.materials import _612

        return self.__parent__._cast(_612.CylindricalGearMaterial)

    @property
    def iso_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_624.ISOCylindricalGearMaterial":
        from mastapy._private.gears.materials import _624

        return self.__parent__._cast(_624.ISOCylindricalGearMaterial)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_material(
        self: "CastSelf",
    ) -> "_629.KlingelnbergCycloPalloidConicalGearMaterial":
        from mastapy._private.gears.materials import _629

        return self.__parent__._cast(_629.KlingelnbergCycloPalloidConicalGearMaterial)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_633.PlasticCylindricalGearMaterial":
        from mastapy._private.gears.materials import _633

        return self.__parent__._cast(_633.PlasticCylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "GearMaterial":
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
class GearMaterial(_288.Material):
    """GearMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def apply_derating_factors_to_bending_custom_sn_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ApplyDeratingFactorsToBendingCustomSNCurve"
        )

        if temp is None:
            return False

        return temp

    @apply_derating_factors_to_bending_custom_sn_curve.setter
    @enforce_parameter_types
    def apply_derating_factors_to_bending_custom_sn_curve(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyDeratingFactorsToBendingCustomSNCurve",
            bool(value) if value is not None else False,
        )

    @property
    def apply_derating_factors_to_contact_custom_sn_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ApplyDeratingFactorsToContactCustomSNCurve"
        )

        if temp is None:
            return False

        return temp

    @apply_derating_factors_to_contact_custom_sn_curve.setter
    @enforce_parameter_types
    def apply_derating_factors_to_contact_custom_sn_curve(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyDeratingFactorsToContactCustomSNCurve",
            bool(value) if value is not None else False,
        )

    @property
    def core_hardness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoreHardness")

        if temp is None:
            return 0.0

        return temp

    @core_hardness.setter
    @enforce_parameter_types
    def core_hardness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoreHardness", float(value) if value is not None else 0.0
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
    def nc_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NCBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def nc_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NCContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_known_points_for_user_sn_curve_bending_stress(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfKnownPointsForUserSNCurveBendingStress"
        )

        if temp is None:
            return 0

        return temp

    @property
    def number_of_known_points_for_user_sn_curve_for_contact_stress(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfKnownPointsForUserSNCurveForContactStress"
        )

        if temp is None:
            return 0

        return temp

    @property
    def sn_curve_bending(self: "Self") -> "_300.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveBending")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def sn_curve_contact(self: "Self") -> "_300.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveContact")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMaterial":
        """Cast to another type.

        Returns:
            _Cast_GearMaterial
        """
        return _Cast_GearMaterial(self)
