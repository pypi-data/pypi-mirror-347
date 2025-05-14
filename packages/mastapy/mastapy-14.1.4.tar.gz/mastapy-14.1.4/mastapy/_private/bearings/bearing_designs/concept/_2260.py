"""ConceptAxialClearanceBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.concept import _2261

_CONCEPT_AXIAL_CLEARANCE_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Concept", "ConceptAxialClearanceBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1938
    from mastapy._private.bearings.bearing_designs import _2192, _2196
    from mastapy._private.bearings.bearing_designs.concept import _2259

    Self = TypeVar("Self", bound="ConceptAxialClearanceBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptAxialClearanceBearing._Cast_ConceptAxialClearanceBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptAxialClearanceBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptAxialClearanceBearing:
    """Special nested class for casting ConceptAxialClearanceBearing to subclasses."""

    __parent__: "ConceptAxialClearanceBearing"

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2261.ConceptClearanceBearing":
        return self.__parent__._cast(_2261.ConceptClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2196.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2196

        return self.__parent__._cast(_2196.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2192.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2192

        return self.__parent__._cast(_2192.BearingDesign)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "ConceptAxialClearanceBearing":
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
class ConceptAxialClearanceBearing(_2261.ConceptClearanceBearing):
    """ConceptAxialClearanceBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_AXIAL_CLEARANCE_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    def model(self: "Self") -> "_1938.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1938", "BearingModel"
        )(value)

    @property
    def node_position(self: "Self") -> "_2259.BearingNodePosition":
        """mastapy.bearings.bearing_designs.concept.BearingNodePosition"""
        temp = pythonnet_property_get(self.wrapped, "NodePosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Concept.BearingNodePosition"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.concept._2259",
            "BearingNodePosition",
        )(value)

    @node_position.setter
    @enforce_parameter_types
    def node_position(self: "Self", value: "_2259.BearingNodePosition") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDesigns.Concept.BearingNodePosition"
        )
        pythonnet_property_set(self.wrapped, "NodePosition", value)

    @property
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    def thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Thickness")

        if temp is None:
            return 0.0

        return temp

    @thickness.setter
    @enforce_parameter_types
    def thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Thickness", float(value) if value is not None else 0.0
        )

    @property
    def x_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XStiffness")

        if temp is None:
            return 0.0

        return temp

    @x_stiffness.setter
    @enforce_parameter_types
    def x_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XStiffness", float(value) if value is not None else 0.0
        )

    @property
    def x_stiffness_applied_only_when_contacting(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "XStiffnessAppliedOnlyWhenContacting"
        )

        if temp is None:
            return False

        return temp

    @x_stiffness_applied_only_when_contacting.setter
    @enforce_parameter_types
    def x_stiffness_applied_only_when_contacting(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "XStiffnessAppliedOnlyWhenContacting",
            bool(value) if value is not None else False,
        )

    @property
    def y_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YStiffness")

        if temp is None:
            return 0.0

        return temp

    @y_stiffness.setter
    @enforce_parameter_types
    def y_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YStiffness", float(value) if value is not None else 0.0
        )

    @property
    def y_stiffness_applied_only_when_contacting(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "YStiffnessAppliedOnlyWhenContacting"
        )

        if temp is None:
            return False

        return temp

    @y_stiffness_applied_only_when_contacting.setter
    @enforce_parameter_types
    def y_stiffness_applied_only_when_contacting(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "YStiffnessAppliedOnlyWhenContacting",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptAxialClearanceBearing":
        """Cast to another type.

        Returns:
            _Cast_ConceptAxialClearanceBearing
        """
        return _Cast_ConceptAxialClearanceBearing(self)
