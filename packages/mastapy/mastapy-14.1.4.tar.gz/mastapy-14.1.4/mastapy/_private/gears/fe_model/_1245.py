"""GearFEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1269

_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_GEAR_FLANKS = python_net_import("SMT.MastaAPI.Gears", "GearFlanks")
_GEAR_FE_MODEL = python_net_import("SMT.MastaAPI.Gears.FEModel", "GearFEModel")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private import _7718
    from mastapy._private.gears import _344
    from mastapy._private.gears.analysis import _1263, _1266
    from mastapy._private.gears.fe_model import _1247
    from mastapy._private.gears.fe_model.conical import _1252
    from mastapy._private.gears.fe_model.cylindrical import _1249

    Self = TypeVar("Self", bound="GearFEModel")
    CastSelf = TypeVar("CastSelf", bound="GearFEModel._Cast_GearFEModel")


__docformat__ = "restructuredtext en"
__all__ = ("GearFEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearFEModel:
    """Special nested class for casting GearFEModel to subclasses."""

    __parent__: "GearFEModel"

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1269.GearImplementationDetail":
        return self.__parent__._cast(_1269.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1266.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1266

        return self.__parent__._cast(_1266.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1263.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1263

        return self.__parent__._cast(_1263.AbstractGearAnalysis)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1249.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1249

        return self.__parent__._cast(_1249.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1252.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1252

        return self.__parent__._cast(_1252.ConicalGearFEModel)

    @property
    def gear_fe_model(self: "CastSelf") -> "GearFEModel":
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
class GearFEModel(_1269.GearImplementationDetail):
    """GearFEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def fe_bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FEBore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fe_bore.setter
    @enforce_parameter_types
    def fe_bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FEBore", value)

    @property
    def include_all_teeth_in_the_fe_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAllTeethInTheFEMesh")

        if temp is None:
            return False

        return temp

    @include_all_teeth_in_the_fe_mesh.setter
    @enforce_parameter_types
    def include_all_teeth_in_the_fe_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAllTeethInTheFEMesh",
            bool(value) if value is not None else False,
        )

    @property
    def element_settings(self: "Self") -> "_1247.GearMeshingElementOptions":
        """mastapy.gears.fe_model.GearMeshingElementOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def calculate_stiffness_from_fe(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateStiffnessFromFE")

    @enforce_parameter_types
    def calculate_stiffness_from_fe_with_progress(
        self: "Self", progress: "_7718.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "CalculateStiffnessFromFE",
            [_TASK_PROGRESS],
            progress.wrapped if progress else None,
        )

    @enforce_parameter_types
    def get_stress_influence_coefficients_from_fe(
        self: "Self", flank: "_344.GearFlanks"
    ) -> None:
        """Method does not return.

        Args:
            flank (mastapy.gears.GearFlanks)
        """
        flank = conversion.mp_to_pn_enum(flank, "SMT.MastaAPI.Gears.GearFlanks")
        pythonnet_method_call_overload(
            self.wrapped, "GetStressInfluenceCoefficientsFromFE", [_GEAR_FLANKS], flank
        )

    @enforce_parameter_types
    def get_stress_influence_coefficients_from_fe_with_progress(
        self: "Self", flank: "_344.GearFlanks", progress: "_7718.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            flank (mastapy.gears.GearFlanks)
            progress (mastapy.TaskProgress)
        """
        flank = conversion.mp_to_pn_enum(flank, "SMT.MastaAPI.Gears.GearFlanks")
        pythonnet_method_call_overload(
            self.wrapped,
            "GetStressInfluenceCoefficientsFromFE",
            [_GEAR_FLANKS, _TASK_PROGRESS],
            flank,
            progress.wrapped if progress else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearFEModel":
        """Cast to another type.

        Returns:
            _Cast_GearFEModel
        """
        return _Cast_GearFEModel(self)
