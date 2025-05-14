"""CylindricalGearISOMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _613, _624

_CYLINDRICAL_GEAR_ISO_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "CylindricalGearISOMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _289
    from mastapy._private.utility.databases import _1885, _1889, _1892

    Self = TypeVar("Self", bound="CylindricalGearISOMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearISOMaterialDatabase._Cast_CylindricalGearISOMaterialDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearISOMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearISOMaterialDatabase:
    """Special nested class for casting CylindricalGearISOMaterialDatabase to subclasses."""

    __parent__: "CylindricalGearISOMaterialDatabase"

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_613.CylindricalGearMaterialDatabase":
        return self.__parent__._cast(_613.CylindricalGearMaterialDatabase)

    @property
    def material_database(self: "CastSelf") -> "_289.MaterialDatabase":
        from mastapy._private.materials import _289

        return self.__parent__._cast(_289.MaterialDatabase)

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
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "CylindricalGearISOMaterialDatabase":
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
class CylindricalGearISOMaterialDatabase(
    _613.CylindricalGearMaterialDatabase[_624.ISOCylindricalGearMaterial]
):
    """CylindricalGearISOMaterialDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ISO_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearISOMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearISOMaterialDatabase
        """
        return _Cast_CylindricalGearISOMaterialDatabase(self)
