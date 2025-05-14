"""ConceptMeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.load_case import _906

_CONCEPT_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase.Concept", "ConceptMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1264, _1270

    Self = TypeVar("Self", bound="ConceptMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ConceptMeshLoadCase._Cast_ConceptMeshLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptMeshLoadCase:
    """Special nested class for casting ConceptMeshLoadCase to subclasses."""

    __parent__: "ConceptMeshLoadCase"

    @property
    def mesh_load_case(self: "CastSelf") -> "_906.MeshLoadCase":
        return self.__parent__._cast(_906.MeshLoadCase)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1270.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1270

        return self.__parent__._cast(_1270.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1264.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1264

        return self.__parent__._cast(_1264.AbstractGearMeshAnalysis)

    @property
    def concept_mesh_load_case(self: "CastSelf") -> "ConceptMeshLoadCase":
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
class ConceptMeshLoadCase(_906.MeshLoadCase):
    """ConceptMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ConceptMeshLoadCase
        """
        return _Cast_ConceptMeshLoadCase(self)
