"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1379 import DynamicForceResults
    from mastapy._private.electric_machines.results._1380 import EfficiencyResults
    from mastapy._private.electric_machines.results._1381 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1382 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1383 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1384 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1385 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1386 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1387 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1388 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1389 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1390 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1391 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1392 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1393 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1394 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1395 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1396 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1398 import LinearDQModel
    from mastapy._private.electric_machines.results._1399 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1400 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1401 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1402 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1403 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1379": ["DynamicForceResults"],
        "_private.electric_machines.results._1380": ["EfficiencyResults"],
        "_private.electric_machines.results._1381": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1382": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1383": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1384": ["ElectricMachineResults"],
        "_private.electric_machines.results._1385": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1386": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1387": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1388": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1389": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1390": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1391": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1392": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1393": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1394": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1395": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1396": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1398": ["LinearDQModel"],
        "_private.electric_machines.results._1399": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1400": ["NonLinearDQModel"],
        "_private.electric_machines.results._1401": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1402": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1403": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
