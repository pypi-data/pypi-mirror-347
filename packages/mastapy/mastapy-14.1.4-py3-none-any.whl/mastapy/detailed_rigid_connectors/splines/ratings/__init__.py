"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1482 import (
        AGMA6123SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1483 import (
        AGMA6123SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1484 import (
        DIN5466SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1485 import (
        DIN5466SplineRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1486 import (
        GBT17855SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1487 import (
        GBT17855SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1488 import (
        SAESplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1489 import (
        SAESplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1490 import (
        SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1491 import (
        SplineJointRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines.ratings._1482": [
            "AGMA6123SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1483": [
            "AGMA6123SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1484": [
            "DIN5466SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1485": [
            "DIN5466SplineRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1486": [
            "GBT17855SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1487": [
            "GBT17855SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1488": [
            "SAESplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1489": [
            "SAESplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1490": [
            "SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1491": [
            "SplineJointRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA6123SplineHalfRating",
    "AGMA6123SplineJointRating",
    "DIN5466SplineHalfRating",
    "DIN5466SplineRating",
    "GBT17855SplineHalfRating",
    "GBT17855SplineJointRating",
    "SAESplineHalfRating",
    "SAESplineJointRating",
    "SplineHalfRating",
    "SplineJointRating",
)
