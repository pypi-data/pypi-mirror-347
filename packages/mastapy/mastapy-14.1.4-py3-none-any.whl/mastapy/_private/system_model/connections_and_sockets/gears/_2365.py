"""BevelDifferentialGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2367

_BEVEL_DIFFERENTIAL_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "BevelDifferentialGearTeethSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2359
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2363,
        _2371,
        _2377,
    )

    Self = TypeVar("Self", bound="BevelDifferentialGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearTeethSocket._Cast_BevelDifferentialGearTeethSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearTeethSocket:
    """Special nested class for casting BevelDifferentialGearTeethSocket to subclasses."""

    __parent__: "BevelDifferentialGearTeethSocket"

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2367.BevelGearTeethSocket":
        return self.__parent__._cast(_2367.BevelGearTeethSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2363.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2363

        return self.__parent__._cast(_2363.AGMAGleasonConicalGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2371.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2371

        return self.__parent__._cast(_2371.ConicalGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2377.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2377

        return self.__parent__._cast(_2377.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2359.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2359

        return self.__parent__._cast(_2359.Socket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "BevelDifferentialGearTeethSocket":
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
class BevelDifferentialGearTeethSocket(_2367.BevelGearTeethSocket):
    """BevelDifferentialGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearTeethSocket
        """
        return _Cast_BevelDifferentialGearTeethSocket(self)
