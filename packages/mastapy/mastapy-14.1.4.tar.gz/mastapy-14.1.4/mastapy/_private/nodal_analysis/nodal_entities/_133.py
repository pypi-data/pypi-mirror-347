"""BarRigidMBD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _132

_BAR_RIGID_MBD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "BarRigidMBD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _137, _148, _149

    Self = TypeVar("Self", bound="BarRigidMBD")
    CastSelf = TypeVar("CastSelf", bound="BarRigidMBD._Cast_BarRigidMBD")


__docformat__ = "restructuredtext en"
__all__ = ("BarRigidMBD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BarRigidMBD:
    """Special nested class for casting BarRigidMBD to subclasses."""

    __parent__: "BarRigidMBD"

    @property
    def bar_mbd(self: "CastSelf") -> "_132.BarMBD":
        return self.__parent__._cast(_132.BarMBD)

    @property
    def component_nodal_composite(self: "CastSelf") -> "_137.ComponentNodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _137

        return self.__parent__._cast(_137.ComponentNodalComposite)

    @property
    def nodal_composite(self: "CastSelf") -> "_148.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_149.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.NodalEntity)

    @property
    def bar_rigid_mbd(self: "CastSelf") -> "BarRigidMBD":
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
class BarRigidMBD(_132.BarMBD):
    """BarRigidMBD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BAR_RIGID_MBD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BarRigidMBD":
        """Cast to another type.

        Returns:
            _Cast_BarRigidMBD
        """
        return _Cast_BarRigidMBD(self)
