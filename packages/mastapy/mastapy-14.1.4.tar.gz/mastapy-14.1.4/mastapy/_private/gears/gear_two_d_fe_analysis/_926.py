"""CylindricalGearMeshTIFFAnalysisDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1270

_CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearMeshTIFFAnalysisDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1264

    Self = TypeVar("Self", bound="CylindricalGearMeshTIFFAnalysisDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshTIFFAnalysisDutyCycle._Cast_CylindricalGearMeshTIFFAnalysisDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshTIFFAnalysisDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshTIFFAnalysisDutyCycle:
    """Special nested class for casting CylindricalGearMeshTIFFAnalysisDutyCycle to subclasses."""

    __parent__: "CylindricalGearMeshTIFFAnalysisDutyCycle"

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1270.GearMeshDesignAnalysis":
        return self.__parent__._cast(_1270.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1264.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1264

        return self.__parent__._cast(_1264.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "CylindricalGearMeshTIFFAnalysisDutyCycle":
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
class CylindricalGearMeshTIFFAnalysisDutyCycle(_1270.GearMeshDesignAnalysis):
    """CylindricalGearMeshTIFFAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshTIFFAnalysisDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshTIFFAnalysisDutyCycle
        """
        return _Cast_CylindricalGearMeshTIFFAnalysisDutyCycle(self)
