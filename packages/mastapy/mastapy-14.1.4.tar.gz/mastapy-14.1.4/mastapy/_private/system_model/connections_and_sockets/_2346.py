"""MountableComponentOuterSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2347

_MOUNTABLE_COMPONENT_OUTER_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "MountableComponentOuterSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2330,
        _2339,
        _2359,
    )

    Self = TypeVar("Self", bound="MountableComponentOuterSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentOuterSocket._Cast_MountableComponentOuterSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentOuterSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentOuterSocket:
    """Special nested class for casting MountableComponentOuterSocket to subclasses."""

    __parent__: "MountableComponentOuterSocket"

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2347.MountableComponentSocket":
        return self.__parent__._cast(_2347.MountableComponentSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2339.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2339

        return self.__parent__._cast(_2339.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2359.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2359

        return self.__parent__._cast(_2359.Socket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2330.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.BearingOuterSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "MountableComponentOuterSocket":
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
class MountableComponentOuterSocket(_2347.MountableComponentSocket):
    """MountableComponentOuterSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_OUTER_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentOuterSocket":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentOuterSocket
        """
        return _Cast_MountableComponentOuterSocket(self)
