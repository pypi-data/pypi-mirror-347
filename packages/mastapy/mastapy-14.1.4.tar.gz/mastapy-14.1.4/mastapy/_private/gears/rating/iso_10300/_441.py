"""ISO10300MeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _565

_ISO10300_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.rating import _385
    from mastapy._private.gears.rating.iso_10300 import _442, _443, _444, _445
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _408

    Self = TypeVar("Self", bound="ISO10300MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300MeshSingleFlankRating._Cast_ISO10300MeshSingleFlankRating",
    )

T = TypeVar("T", bound="_408.VirtualCylindricalGearBasic")

__docformat__ = "restructuredtext en"
__all__ = ("ISO10300MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300MeshSingleFlankRating:
    """Special nested class for casting ISO10300MeshSingleFlankRating to subclasses."""

    __parent__: "ISO10300MeshSingleFlankRating"

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_565.ConicalMeshSingleFlankRating":
        return self.__parent__._cast(_565.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_385.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _385

        return self.__parent__._cast(_385.MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_442.ISO10300MeshSingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _442

        return self.__parent__._cast(_442.ISO10300MeshSingleFlankRatingBevelMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_443.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _443

        return self.__parent__._cast(_443.ISO10300MeshSingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_444.ISO10300MeshSingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _444

        return self.__parent__._cast(_444.ISO10300MeshSingleFlankRatingMethodB1)

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_445.ISO10300MeshSingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _445

        return self.__parent__._cast(_445.ISO10300MeshSingleFlankRatingMethodB2)

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO10300MeshSingleFlankRating":
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
class ISO10300MeshSingleFlankRating(_565.ConicalMeshSingleFlankRating, Generic[T]):
    """ISO10300MeshSingleFlankRating

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ISO10300_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def accuracy_grade_according_to_iso17485(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccuracyGradeAccordingToISO17485")

        if temp is None:
            return 0.0

        return temp

    @property
    def application_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def auxiliary_factor_a_for_calculating_the_dynamic_factor_kvc(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryFactorAForCalculatingTheDynamicFactorKVC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def auxiliary_factor_x_for_calculating_the_dynamic_factor_kvc(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryFactorXForCalculatingTheDynamicFactorKVC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def correction_factor_of_tooth_stiffness_for_non_average_conditions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CorrectionFactorOfToothStiffnessForNonAverageConditions"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_1_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv1DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_12_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv12DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_2_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv2DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_3_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv3DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_4_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv4DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_5_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv5DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_56_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv56DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_6_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv6DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cv_7_dynamic_factor_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cv7DynamicFactorInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def dimensionless_reference_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DimensionlessReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorForMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_b_intermediate_sector(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicFactorForMethodBIntermediateSector"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_b_main_resonance_sector(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicFactorForMethodBMainResonanceSector"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_b_sub_critical_sector(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicFactorForMethodBSubCriticalSector"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_b_super_critical_sector(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicFactorForMethodBSuperCriticalSector"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_factor_for_method_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorForMethodC")

        if temp is None:
            return 0.0

        return temp

    @property
    def effective_pitch_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectivePitchDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def elasticity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def exponent_in_the_formula_for_lengthwise_curvature_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ExponentInTheFormulaForLengthwiseCurvatureFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def face_load_factor_for_method_c_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorForMethodCContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def factor_for_calculating_the_dynamic_factor_kvb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FactorForCalculatingTheDynamicFactorKVB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def lead_angle_of_face_hobbing_cutter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadAngleOfFaceHobbingCutter")

        if temp is None:
            return 0.0

        return temp

    @property
    def lengthwise_curvature_factor_for_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthwiseCurvatureFactorForBendingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def lengthwise_tooth_mean_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthwiseToothMeanRadiusOfCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def max_single_pitch_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxSinglePitchDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def max_wheel_tangential_speed_at_outer_end_heel_of_the_reference_cone(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaxWheelTangentialSpeedAtOuterEndHeelOfTheReferenceCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_relative_roughness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanRelativeRoughness")

        if temp is None:
            return 0.0

        return temp

    @property
    def modulus_of_elasticity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @property
    def nominal_tangential_force_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalTangentialForceOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_running_in_allowance_for_through_hardened_steels(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionRunningInAllowanceForThroughHardenedSteels"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def preliminary_transverse_load_factor_for_contact_method_b(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PreliminaryTransverseLoadFactorForContactMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def preliminary_transverse_load_factor_for_contact_method_c(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PreliminaryTransverseLoadFactorForContactMethodC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    def relative_hypoid_offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeHypoidOffset")

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_mass_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMassPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def resonance_speed_of_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResonanceSpeedOfPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    def running_in_allowance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunningInAllowance")

        if temp is None:
            return 0.0

        return temp

    @property
    def running_in_allowance_for_case_hardened_and_nitrided_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RunningInAllowanceForCaseHardenedAndNitridedGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def running_in_allowance_for_grey_cast_iron(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunningInAllowanceForGreyCastIron")

        if temp is None:
            return 0.0

        return temp

    @property
    def single_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    def tangential_force_at_mid_face_width_on_the_pitch_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TangentialForceAtMidFaceWidthOnThePitchCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_for_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorForBendingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_for_bending_stress_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorForBendingStressMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_for_bending_stress_method_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorForBendingStressMethodC"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_for_bevel_gear_with_virtual_contact_ratio_greater_than_2(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "TransverseLoadFactorForBevelGearWithVirtualContactRatioGreaterThan2",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factor_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseLoadFactorForContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_load_factors_for_bevel_gear_with_virtual_contact_ratio_less_or_equal_to_2(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "TransverseLoadFactorsForBevelGearWithVirtualContactRatioLessOrEqualTo2",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_running_in_allowance_for_through_hardened_steels(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelRunningInAllowanceForThroughHardenedSteels"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_tangential_speed_at_outer_end_heel_of_the_reference_cone(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelTangentialSpeedAtOuterEndHeelOfTheReferenceCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def eta_1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Eta1")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO10300MeshSingleFlankRating
        """
        return _Cast_ISO10300MeshSingleFlankRating(self)
