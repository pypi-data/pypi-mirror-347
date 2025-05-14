"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.cad_export._1893 import CADExportSettings
    from mastapy._private.utility.cad_export._1894 import StockDrawings
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.cad_export._1893": ["CADExportSettings"],
        "_private.utility.cad_export._1894": ["StockDrawings"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CADExportSettings",
    "StockDrawings",
)
