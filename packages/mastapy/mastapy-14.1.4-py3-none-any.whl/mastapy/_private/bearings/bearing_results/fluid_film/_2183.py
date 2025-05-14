"""LoadedPadFluidFilmBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results.fluid_film import _2181

_LOADED_PAD_FLUID_FILM_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedPadFluidFilmBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1936
    from mastapy._private.bearings.bearing_results import _2011, _2016, _2019
    from mastapy._private.bearings.bearing_results.fluid_film import _2189, _2190

    Self = TypeVar("Self", bound="LoadedPadFluidFilmBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedPadFluidFilmBearingResults._Cast_LoadedPadFluidFilmBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedPadFluidFilmBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedPadFluidFilmBearingResults:
    """Special nested class for casting LoadedPadFluidFilmBearingResults to subclasses."""

    __parent__: "LoadedPadFluidFilmBearingResults"

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2181.LoadedFluidFilmBearingResults":
        return self.__parent__._cast(_2181.LoadedFluidFilmBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2016.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2016

        return self.__parent__._cast(_2016.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2019.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2019

        return self.__parent__._cast(_2019.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2011.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2011

        return self.__parent__._cast(_2011.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_1936.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _1936

        return self.__parent__._cast(_1936.BearingLoadCaseResultsLightweight)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2189.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2189

        return self.__parent__._cast(_2189.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2190.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2190

        return self.__parent__._cast(_2190.LoadedTiltingPadThrustBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "LoadedPadFluidFilmBearingResults":
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
class LoadedPadFluidFilmBearingResults(_2181.LoadedFluidFilmBearingResults):
    """LoadedPadFluidFilmBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_PAD_FLUID_FILM_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def minimum_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def oil_inlet_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilInletTemperature")

        if temp is None:
            return 0.0

        return temp

    @oil_inlet_temperature.setter
    @enforce_parameter_types
    def oil_inlet_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilInletTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def reynolds_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReynoldsNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedPadFluidFilmBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedPadFluidFilmBearingResults
        """
        return _Cast_LoadedPadFluidFilmBearingResults(self)
