"""AnalysisSettingsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis import _53
from mastapy._private.utility.databases import _1889

_ANALYSIS_SETTINGS_DATABASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "AnalysisSettingsDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1885, _1892

    Self = TypeVar("Self", bound="AnalysisSettingsDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="AnalysisSettingsDatabase._Cast_AnalysisSettingsDatabase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisSettingsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisSettingsDatabase:
    """Special nested class for casting AnalysisSettingsDatabase to subclasses."""

    __parent__: "AnalysisSettingsDatabase"

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
    def analysis_settings_database(self: "CastSelf") -> "AnalysisSettingsDatabase":
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
class AnalysisSettingsDatabase(_1889.NamedDatabase[_53.AnalysisSettingsItem]):
    """AnalysisSettingsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_SETTINGS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AnalysisSettingsDatabase":
        """Cast to another type.

        Returns:
            _Cast_AnalysisSettingsDatabase
        """
        return _Cast_AnalysisSettingsDatabase(self)
