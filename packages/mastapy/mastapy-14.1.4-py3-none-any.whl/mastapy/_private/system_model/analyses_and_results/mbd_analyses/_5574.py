"""MBDAnalysisDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.drawing import _2309

_MBD_ANALYSIS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "MBDAnalysisDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _326

    Self = TypeVar("Self", bound="MBDAnalysisDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="MBDAnalysisDrawStyle._Cast_MBDAnalysisDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MBDAnalysisDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MBDAnalysisDrawStyle:
    """Special nested class for casting MBDAnalysisDrawStyle to subclasses."""

    __parent__: "MBDAnalysisDrawStyle"

    @property
    def contour_draw_style(self: "CastSelf") -> "_2309.ContourDrawStyle":
        return self.__parent__._cast(_2309.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_326.DrawStyleBase":
        from mastapy._private.geometry import _326

        return self.__parent__._cast(_326.DrawStyleBase)

    @property
    def mbd_analysis_draw_style(self: "CastSelf") -> "MBDAnalysisDrawStyle":
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
class MBDAnalysisDrawStyle(_2309.ContourDrawStyle):
    """MBDAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MBD_ANALYSIS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MBDAnalysisDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_MBDAnalysisDrawStyle
        """
        return _Cast_MBDAnalysisDrawStyle(self)
