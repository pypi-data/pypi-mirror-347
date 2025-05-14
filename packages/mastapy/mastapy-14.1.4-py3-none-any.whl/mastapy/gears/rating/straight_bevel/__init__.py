"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.straight_bevel._414 import (
        StraightBevelGearMeshRating,
    )
    from mastapy._private.gears.rating.straight_bevel._415 import (
        StraightBevelGearRating,
    )
    from mastapy._private.gears.rating.straight_bevel._416 import (
        StraightBevelGearSetRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.straight_bevel._414": ["StraightBevelGearMeshRating"],
        "_private.gears.rating.straight_bevel._415": ["StraightBevelGearRating"],
        "_private.gears.rating.straight_bevel._416": ["StraightBevelGearSetRating"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "StraightBevelGearMeshRating",
    "StraightBevelGearRating",
    "StraightBevelGearSetRating",
)
