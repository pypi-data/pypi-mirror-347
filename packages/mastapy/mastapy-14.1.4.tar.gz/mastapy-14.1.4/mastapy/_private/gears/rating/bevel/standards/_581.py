"""SpiralBevelMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _565

_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards", "SpiralBevelMeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _385
    from mastapy._private.gears.rating.bevel.standards import _577, _579

    Self = TypeVar("Self", bound="SpiralBevelMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelMeshSingleFlankRating._Cast_SpiralBevelMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelMeshSingleFlankRating:
    """Special nested class for casting SpiralBevelMeshSingleFlankRating to subclasses."""

    __parent__: "SpiralBevelMeshSingleFlankRating"

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
    def agma_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_577.AGMASpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _577

        return self.__parent__._cast(_577.AGMASpiralBevelMeshSingleFlankRating)

    @property
    def gleason_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_579.GleasonSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _579

        return self.__parent__._cast(_579.GleasonSpiralBevelMeshSingleFlankRating)

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "SpiralBevelMeshSingleFlankRating":
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
class SpiralBevelMeshSingleFlankRating(_565.ConicalMeshSingleFlankRating):
    """SpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def dynamic_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def dynamic_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def elastic_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor_i(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorI")

        if temp is None:
            return 0.0

        return temp

    @property
    def inertia_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def length_of_line_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfLineOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_distribution_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_distribution_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_sharing_ratio_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingRatioContact")

        if temp is None:
            return 0.0

        return temp

    @property
    def overload_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def overload_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverloadFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def pitch_line_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchLineVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def pitting_resistance_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PittingResistanceGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def reliability_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def reliability_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def temperature_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def temperature_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    def transmitted_tangential_load_at_large_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransmittedTangentialLoadAtLargeEnd"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelMeshSingleFlankRating
        """
        return _Cast_SpiralBevelMeshSingleFlankRating(self)
