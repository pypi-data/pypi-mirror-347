"""CylindricalWormGrinderDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical import _641
from mastapy._private.gears.manufacturing.cylindrical.cutters import _739

_CYLINDRICAL_WORM_GRINDER_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalWormGrinderDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1885, _1889, _1892

    Self = TypeVar("Self", bound="CylindricalWormGrinderDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalWormGrinderDatabase._Cast_CylindricalWormGrinderDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalWormGrinderDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalWormGrinderDatabase:
    """Special nested class for casting CylindricalWormGrinderDatabase to subclasses."""

    __parent__: "CylindricalWormGrinderDatabase"

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_641.CylindricalCutterDatabase":
        return self.__parent__._cast(_641.CylindricalCutterDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1889.NamedDatabase":
        from mastapy._private.utility.databases import _1889

        return self.__parent__._cast(_1889.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1892.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1892

        return self.__parent__._cast(_1892.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1885.Database":
        pass

        from mastapy._private.utility.databases import _1885

        return self.__parent__._cast(_1885.Database)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "CylindricalWormGrinderDatabase":
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
class CylindricalWormGrinderDatabase(
    _641.CylindricalCutterDatabase[_739.CylindricalGearGrindingWorm]
):
    """CylindricalWormGrinderDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_WORM_GRINDER_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalWormGrinderDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalWormGrinderDatabase
        """
        return _Cast_CylindricalWormGrinderDatabase(self)
