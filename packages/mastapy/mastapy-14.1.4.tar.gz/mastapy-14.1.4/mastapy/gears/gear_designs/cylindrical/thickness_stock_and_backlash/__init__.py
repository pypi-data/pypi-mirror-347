"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1130 import (
        FinishStockSpecification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1131 import (
        FinishStockType,
    )
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1132 import (
        NominalValueSpecification,
    )
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1133 import (
        NoValueSpecification,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1130": [
            "FinishStockSpecification"
        ],
        "_private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1131": [
            "FinishStockType"
        ],
        "_private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1132": [
            "NominalValueSpecification"
        ],
        "_private.gears.gear_designs.cylindrical.thickness_stock_and_backlash._1133": [
            "NoValueSpecification"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FinishStockSpecification",
    "FinishStockType",
    "NominalValueSpecification",
    "NoValueSpecification",
)
