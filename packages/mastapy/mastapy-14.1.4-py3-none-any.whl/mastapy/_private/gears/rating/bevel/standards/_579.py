"""GleasonSpiralBevelMeshSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.bevel.standards import _581

_GLEASON_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards",
    "GleasonSpiralBevelMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _385
    from mastapy._private.gears.rating.bevel.standards import _578
    from mastapy._private.gears.rating.conical import _565

    Self = TypeVar("Self", bound="GleasonSpiralBevelMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GleasonSpiralBevelMeshSingleFlankRating._Cast_GleasonSpiralBevelMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GleasonSpiralBevelMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GleasonSpiralBevelMeshSingleFlankRating:
    """Special nested class for casting GleasonSpiralBevelMeshSingleFlankRating to subclasses."""

    __parent__: "GleasonSpiralBevelMeshSingleFlankRating"

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_581.SpiralBevelMeshSingleFlankRating":
        return self.__parent__._cast(_581.SpiralBevelMeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_565.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _565

        return self.__parent__._cast(_565.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_385.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _385

        return self.__parent__._cast(_385.MeshSingleFlankRating)

    @property
    def gleason_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "GleasonSpiralBevelMeshSingleFlankRating":
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
class GleasonSpiralBevelMeshSingleFlankRating(_581.SpiralBevelMeshSingleFlankRating):
    """GleasonSpiralBevelMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GLEASON_SPIRAL_BEVEL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def allowable_scoring_index(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableScoringIndex")

        if temp is None:
            return 0.0

        return temp

    @property
    def assumed_maximum_pinion_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssumedMaximumPinionTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_ellipse_width_instantaneous(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactEllipseWidthInstantaneous")

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor_g(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorG")

        if temp is None:
            return 0.0

        return temp

    @property
    def load_factor_scoring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactorScoring")

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
    def safety_factor_scoring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorScoring")

        if temp is None:
            return 0.0

        return temp

    @property
    def scoring_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScoringFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def temperature_rise_at_critical_point_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureRiseAtCriticalPointOfContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def thermal_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_578.GleasonSpiralBevelGearSingleFlankRating]":
        """List[mastapy.gears.rating.bevel.standards.GleasonSpiralBevelGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def gleason_bevel_gear_single_flank_ratings(
        self: "Self",
    ) -> "List[_578.GleasonSpiralBevelGearSingleFlankRating]":
        """List[mastapy.gears.rating.bevel.standards.GleasonSpiralBevelGearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GleasonBevelGearSingleFlankRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GleasonSpiralBevelMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_GleasonSpiralBevelMeshSingleFlankRating
        """
        return _Cast_GleasonSpiralBevelMeshSingleFlankRating(self)
