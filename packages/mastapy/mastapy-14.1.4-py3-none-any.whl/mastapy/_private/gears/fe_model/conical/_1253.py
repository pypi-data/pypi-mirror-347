"""ConicalMeshFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.fe_model import _1246

_CONICAL_MESH_FE_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Conical", "ConicalMeshFEModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1264, _1270, _1273

    Self = TypeVar("Self", bound="ConicalMeshFEModel")
    CastSelf = TypeVar("CastSelf", bound="ConicalMeshFEModel._Cast_ConicalMeshFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshFEModel:
    """Special nested class for casting ConicalMeshFEModel to subclasses."""

    __parent__: "ConicalMeshFEModel"

    @property
    def gear_mesh_fe_model(self: "CastSelf") -> "_1246.GearMeshFEModel":
        return self.__parent__._cast(_1246.GearMeshFEModel)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1273.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1273

        return self.__parent__._cast(_1273.GearMeshImplementationDetail)

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
    def conical_mesh_fe_model(self: "CastSelf") -> "ConicalMeshFEModel":
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
class ConicalMeshFEModel(_1246.GearMeshFEModel):
    """ConicalMeshFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshFEModel":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshFEModel
        """
        return _Cast_ConicalMeshFEModel(self)
