"""GearMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2344

_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _981
    from mastapy._private.system_model import _2266
    from mastapy._private.system_model.connections_and_sockets import _2335
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2372,
        _2374,
        _2378,
        _2381,
        _2382,
        _2383,
        _2386,
        _2388,
        _2390,
        _2392,
        _2394,
    )

    Self = TypeVar("Self", bound="GearMesh")
    CastSelf = TypeVar("CastSelf", bound="GearMesh._Cast_GearMesh")


__docformat__ = "restructuredtext en"
__all__ = ("GearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMesh:
    """Special nested class for casting GearMesh to subclasses."""

    __parent__: "GearMesh"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2344.InterMountableComponentConnection":
        return self.__parent__._cast(_2344.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2335.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2266.DesignEntity":
        from mastapy._private.system_model import _2266

        return self.__parent__._cast(_2266.DesignEntity)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2362.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2364.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2366.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2368.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2370.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2372.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2374.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.FaceGearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2378.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2381.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2381

        return self.__parent__._cast(_2381.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2382.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2383.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2383

        return self.__parent__._cast(_2383.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2386.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2386

        return self.__parent__._cast(_2386.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2388.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2388

        return self.__parent__._cast(_2388.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2390.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2390

        return self.__parent__._cast(_2390.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2392.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2392

        return self.__parent__._cast(_2392.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2394.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2394

        return self.__parent__._cast(_2394.ZerolBevelGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "GearMesh":
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
class GearMesh(_2344.InterMountableComponentConnection):
    """GearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mesh_efficiency(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MeshEfficiency")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mesh_efficiency.setter
    @enforce_parameter_types
    def mesh_efficiency(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MeshEfficiency", value)

    @property
    def use_specified_mesh_stiffness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSpecifiedMeshStiffness")

        if temp is None:
            return False

        return temp

    @use_specified_mesh_stiffness.setter
    @enforce_parameter_types
    def use_specified_mesh_stiffness(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSpecifiedMeshStiffness",
            bool(value) if value is not None else False,
        )

    @property
    def user_specified_mesh_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @user_specified_mesh_stiffness.setter
    @enforce_parameter_types
    def user_specified_mesh_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedMeshStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    def active_gear_mesh_design(self: "Self") -> "_981.GearMeshDesign":
        """mastapy.gears.gear_designs.GearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMesh":
        """Cast to another type.

        Returns:
            _Cast_GearMesh
        """
        return _Cast_GearMesh(self)
