"""CylindricalGearDesignConstraintsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1052
from mastapy._private.utility.databases import _1889

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalGearDesignConstraintsDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1885, _1892

    Self = TypeVar("Self", bound="CylindricalGearDesignConstraintsDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignConstraintsDatabase._Cast_CylindricalGearDesignConstraintsDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignConstraintsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignConstraintsDatabase:
    """Special nested class for casting CylindricalGearDesignConstraintsDatabase to subclasses."""

    __parent__: "CylindricalGearDesignConstraintsDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1889.NamedDatabase":
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
    def cylindrical_gear_design_constraints_database(
        self: "CastSelf",
    ) -> "CylindricalGearDesignConstraintsDatabase":
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
class CylindricalGearDesignConstraintsDatabase(
    _1889.NamedDatabase[_1052.CylindricalGearDesignConstraints]
):
    """CylindricalGearDesignConstraintsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignConstraintsDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignConstraintsDatabase
        """
        return _Cast_CylindricalGearDesignConstraintsDatabase(self)
