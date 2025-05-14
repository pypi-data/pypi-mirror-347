"""ISO10300SingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _562

_ISO10300_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.rating import _383
    from mastapy._private.gears.rating.iso_10300 import _449, _450, _451, _452
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _408

    Self = TypeVar("Self", bound="ISO10300SingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO10300SingleFlankRating._Cast_ISO10300SingleFlankRating"
    )

T = TypeVar("T", bound="_408.VirtualCylindricalGearBasic")

__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRating:
    """Special nested class for casting ISO10300SingleFlankRating to subclasses."""

    __parent__: "ISO10300SingleFlankRating"

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_562.ConicalGearSingleFlankRating":
        return self.__parent__._cast(_562.ConicalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_383.GearSingleFlankRating":
        from mastapy._private.gears.rating import _383

        return self.__parent__._cast(_383.GearSingleFlankRating)

    @property
    def iso10300_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_449.ISO10300SingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _449

        return self.__parent__._cast(_449.ISO10300SingleFlankRatingBevelMethodB2)

    @property
    def iso10300_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_450.ISO10300SingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _450

        return self.__parent__._cast(_450.ISO10300SingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_451.ISO10300SingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _451

        return self.__parent__._cast(_451.ISO10300SingleFlankRatingMethodB1)

    @property
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_452.ISO10300SingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _452

        return self.__parent__._cast(_452.ISO10300SingleFlankRatingMethodB2)

    @property
    def iso10300_single_flank_rating(self: "CastSelf") -> "ISO10300SingleFlankRating":
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
class ISO10300SingleFlankRating(_562.ConicalGearSingleFlankRating, Generic[T]):
    """ISO10300SingleFlankRating

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_contact_stress_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStressNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_stress_number_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def constant_lubricant_film_factor_czl_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConstantLubricantFilmFactorCZLMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def constant_roughness_factor_czr_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstantRoughnessFactorCZRMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    def constant_speed_factor_czv_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstantSpeedFactorCZVMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    def life_factor_for_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def life_factor_for_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def lubricant_factor_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalPower")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_tangential_force_of_bevel_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalTangentialForceOfBevelGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_tangential_speed_at_mean_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTangentialSpeedAtMeanPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def product_of_lubricant_film_influence_factors(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProductOfLubricantFilmInfluenceFactors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_mass_per_unit_face_width_reference_to_line_of_action(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeMassPerUnitFaceWidthReferenceToLineOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_surface_condition_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeSurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def roughness_factor_for_contact_stress_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RoughnessFactorForContactStressMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def single_pitch_deviation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SinglePitchDeviation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def size_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def size_factor_for_case_flame_induction_hardened_steels_nitrided_or_nitro_carburized_steels(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SizeFactorForCaseFlameInductionHardenedSteelsNitridedOrNitroCarburizedSteels",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def size_factor_for_grey_cast_iron_and_spheroidal_cast_iron(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SizeFactorForGreyCastIronAndSpheroidalCastIron"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def size_factor_for_structural_and_through_hardened_steels_spheroidal_cast_iron_perlitic_malleable_cast_iron(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SizeFactorForStructuralAndThroughHardenedSteelsSpheroidalCastIronPerliticMalleableCastIron",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def speed_factor_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    def work_hardening_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkHardeningFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRating
        """
        return _Cast_ISO10300SingleFlankRating(self)
