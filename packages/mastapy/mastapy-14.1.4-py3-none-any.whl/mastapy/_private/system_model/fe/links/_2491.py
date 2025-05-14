"""PlanetBasedFELink"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2489

_PLANET_BASED_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "PlanetBasedFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2482, _2486, _2490, _2492

    Self = TypeVar("Self", bound="PlanetBasedFELink")
    CastSelf = TypeVar("CastSelf", bound="PlanetBasedFELink._Cast_PlanetBasedFELink")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetBasedFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetBasedFELink:
    """Special nested class for casting PlanetBasedFELink to subclasses."""

    __parent__: "PlanetBasedFELink"

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2489.MultiNodeFELink":
        return self.__parent__._cast(_2489.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2482.FELink":
        from mastapy._private.system_model.fe.links import _2482

        return self.__parent__._cast(_2482.FELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2486.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2486

        return self.__parent__._cast(_2486.GearWithDuplicatedMeshesFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2490.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2490

        return self.__parent__._cast(_2490.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2492.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2492

        return self.__parent__._cast(_2492.PlanetCarrierFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "PlanetBasedFELink":
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
class PlanetBasedFELink(_2489.MultiNodeFELink):
    """PlanetBasedFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_BASED_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetBasedFELink":
        """Cast to another type.

        Returns:
            _Cast_PlanetBasedFELink
        """
        return _Cast_PlanetBasedFELink(self)
