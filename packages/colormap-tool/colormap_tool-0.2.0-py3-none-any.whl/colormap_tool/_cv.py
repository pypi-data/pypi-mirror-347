"""OpenCV colormap utilities.

This module provides functions to retrieve colormaps in a format suitable for use with OpenCV.
It can return both built-in OpenCV colormaps (as integer constants) and custom colormaps
from other sources (as numpy arrays).
"""

from typing import Optional

import numpy as np

from colormap_tool._cmps import CMPSPACE

__all__ = ["get_cv_colormaps"]


def get_cv_colormaps(name: str, namespace: Optional[str] = None, return_arr: bool = False) -> int | np.ndarray:
    """
    Get a BGR colormap in OpenCV format.

    Note: The returned array is not in RGB format, but in BGR format!

    Parameters
    ----------
    name : str
        The name of the colormap. If namespace is None, this should be in the format
        "namespace.name" (e.g., "cv.VIRIDIS", "mpl.viridis").
    namespace : Optional[str], optional
        The namespace of the colormap ("cv", "mpl"). If provided, the name
        parameter should not include the namespace prefix.
    return_arr : bool, optional
        If True, always returns a numpy array, even for built-in OpenCV colormaps.
        If False, returns an integer constant for built-in OpenCV colormaps and a numpy
        array for other colormaps.
        Default is False.

    Returns
    -------
    int or numpy.ndarray
        For OpenCV built-in colormaps (namespace="cv"), returns the integer constant
        that can be passed to cv2.applyColorMap().
        For other colormaps, returns a numpy array with shape (256, 1, 3) and dtype uint8
        that can be used with cv2.applyColorMap(img, colormap).

    Raises
    ------
    AssertionError
        If the namespace is not recognized or the colormap name is not found in the namespace.

    Examples
    --------
    >>> # Get an OpenCV built-in colormap
    >>> cmap = get_cv_colormaps("VIRIDIS", "cv")
    >>> # Or equivalently
    >>> cmap = get_cv_colormaps("cv.VIRIDIS")
    >>> colored_img = cv2.applyColorMap(gray_img, cmap)

    >>> # Get a matplotlib colormap for use with OpenCV
    >>> cmap = get_cv_colormaps("viridis", "mpl")
    >>> # Or equivalently
    >>> cmap = get_cv_colormaps("mpl.viridis")
    >>> colored_img = cv2.applyColorMap(gray_img, cmap)
    """
    try:
        import cv2
    except ImportError:
        cv2 = None
    if namespace is not None:
        if "." in name:
            raise ValueError(f"Namespace {namespace} is provided, so name {name} should not include a dot.")
    else:
        namespace, name = name.split(".")

    namespace = namespace.lower()
    name = name.lower()
    if namespace not in CMPSPACE:
        raise ValueError(f"Namespace {namespace} is not recognized.")
    if name not in CMPSPACE[namespace]:
        raise ValueError(f"Colormap {name} is not found in namespace {namespace}.")

    if namespace == "cv" and not return_arr and cv2 is not None:
        return cv2.__dict__[f"COLORMAP_{name.upper()}"]
    else:
        rgb_arr = CMPSPACE[namespace][name]
        bgr_arr = rgb_arr[:, :, ::-1]
        return bgr_arr


def apply_colormap_with_numpy(src: np.ndarray, cmp: np.ndarray, dst: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Apply a colormap to an image using numpy instead of OpenCV.

    Parameters
    ----------
    src : numpy.ndarray
        The image to apply the colormap to.
    cmp : numpy.ndarray
        The colormap to apply. Should have shape (256, 1, 3) and dtype uint8.
    dst : numpy.ndarray, optional
        The output array to store the result. If None, a new array will be created.

    Returns
    -------
    numpy.ndarray
        The output array with the colormap applied.
    """
    if dst is None:
        dst = np.zeros_like(src)
    else:
        if dst.shape != src.shape:
            raise ValueError(
                f"The shape of the output array {dst.shape} does not match the shape of the input array {src.shape}."
            )

    if src.dtype != np.uint8:
        raise ValueError(f"The dtype of the input array {src.dtype} is not uint8.")
    if cmp.shape != (256, 1, 3):
        raise ValueError(f"The shape of the colormap array {cmp.shape} is not (256, 1, 3).")
    if cmp.dtype != np.uint8:
        raise ValueError(f"The dtype of the colormap array {cmp.dtype} is not uint8.")

    dst = cmp.copy().squeeze()
    dst = dst[src]

    return dst
