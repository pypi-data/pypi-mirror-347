"""
Colormap storage and loading module.

This module loads colormap data from pickle files stored in the resources directory.
Each colormap is stored as a numpy array with shape (256, 1, 3) and dtype uint8.
The module provides access to colormaps from different sources (matplotlib, OpenCV).

The colormaps are loaded at import time and stored in dictionaries for easy access.
"""

import importlib.resources
import pickle

import numpy as np

RESOURCES_DIR = importlib.resources.files("colormap_tool").joinpath("resources")

with (RESOURCES_DIR / "mpl_colormaps.pickle").open("rb") as f:
    MPL_COLORMAPS: dict[str, np.ndarray] = pickle.load(f)


with (RESOURCES_DIR / "cv_colormaps.pickle").open("rb") as f:
    CV_COLORMAPS: dict[str, np.ndarray] = pickle.load(f)


CMPSPACE = {
    "cv": CV_COLORMAPS,
    "mpl": MPL_COLORMAPS,
}


__all__ = ["CMPSPACE", "CV_COLORMAPS", "MPL_COLORMAPS"]
