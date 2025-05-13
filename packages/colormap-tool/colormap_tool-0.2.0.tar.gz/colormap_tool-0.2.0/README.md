# colormap-tool

[![Release](https://img.shields.io/github/v/release/MeridianInnovation/colormap-tool)](https://img.shields.io/github/v/release/MeridianInnovation/colormap-tool)
[![Commit activity](https://img.shields.io/github/commit-activity/m/MeridianInnovation/colormap-tool)](https://img.shields.io/github/commit-activity/m/MeridianInnovation/colormap-tool)
[![License](https://img.shields.io/github/license/MeridianInnovation/colormap-tool)](https://img.shields.io/github/license/MeridianInnovation/colormap-tool)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10%2C%3C%3D3.13-blue)](https://img.shields.io/badge/python-%3E%3D3.10%2C%3C%3D3.13-blue)

A Colormap Tool package to convert cmps between cv and mpl.

- **Github repository**: <https://github.com/MeridianInnovation/colormap-tool/>
- **Documentation** <https://MeridianInnovation.github.io/colormap-tool/>

## Overview

This package can let users use cv's built-in colormap in matplotlib, or use matplotlib's colormap in cv.

## Features

- Convert colormaps between matplotlib and OpenCV formats
- Access colormaps from matplotlib and OpenCVs through a common interface
- Convert between numpy arrays, matplotlib Colormap objects, and OpenCV constants
- Register external colormaps with matplotlib

## Installation

To install the project, run the following command:

```bash
python -m pip install colormap-tool
```

## Usage

### Basic Import

```python
import cv2
import matplotlib.pyplot as plt
import numpy as np
import colormap_tools
```

### Available Colormap Namespaces

The package provides colormaps from three sources:

- `cv`: OpenCV built-in colormaps (e.g., `viridis`, `plasma`, `jet`)
- `mpl`: Matplotlib built-in colormaps (e.g., `viridis`, `plasma`, `jet`)

### Accessing Colormaps

There are two ways to specify which colormap you want:

1. Using separate namespace and name parameters:

```python
# Get a matplotlib colormap
cmap = colormap_tools.get_cv_colormaps("viridis", "mpl")
# Get an OpenCV colormap
cmap = colormap_tools.get_mpl_colormaps("viridis", "cv")
```

2. Using dot notation in a single parameter:

```python
# Get a matplotlib colormap
cmap = colormap_tools.get_cv_colormaps("mpl.viridis")
# Get an OpenCV colormap
cmap = colormap_tools.get_mpl_colormaps("cv.viridis")
```

### Using Colormaps with OpenCV

```python
# Get a matplotlib colormap for use with OpenCV
# Note: This method returns a BGR format colormap!
cmap = colormap_tools.get_cv_colormaps("viridis", "mpl")

# Create a sample grayscale image
gray_img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

# Apply the colormap
colored_img = cv2.applyColorMap(gray_img, cmap)

# Display the image (note: OpenCV uses BGR format)
colored_img_rgb = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)  # Convert to RGB for display
cv2.imshow("Colored Image", colored_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Using Colormaps with Matplotlib

```python
# Get an OpenCV colormap for use with matplotlib
cmap = colormap_tools.get_mpl_colormaps("viridis", "cv")

from matplotlib.colors import Colormap
assert isinstance(cmap, Colormap)

# Create a sample grayscale image
gray_img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

# Display the image with the colormap
plt.figure(figsize=(6, 6))
plt.imshow(gray_img, cmap=cmap)
plt.colorbar(label="Value")
plt.title("Image with OpenCV VIRIDIS colormap")
plt.show()
```

### Registering Colormaps with Matplotlib

You can register all colormaps with matplotlib for direct access by name:

```python
# Register all colormaps with matplotlib
colormap_tools.register_all_cmps2mpl()

# Now you can use any colormap directly with matplotlib by name
plt.figure(figsize=(12, 4))

# Create a sample data array
data = np.random.rand(20, 20)

# Plot with different colormaps
plt.subplot(121)
plt.imshow(data, cmap="cv.jet") # do not use cv.JET
plt.title("OpenCV JET")
plt.colorbar()

plt.subplot(122)
plt.imshow(data, cmap="viridis") # do not use mpl.viridis
plt.title("Matplotlib Viridis")
plt.colorbar()

plt.tight_layout()
plt.show()
```

### Converting RGB Arrays to Matplotlib Colormaps

If you have your own RGB colormap data, you can convert it to a matplotlib colormap:

```python
# Create a custom RGB array (256×3 uint8 values)
rgb_data = np.zeros((256, 3), dtype=np.uint8)
# Fill with a gradient from blue to red
rgb_data[:, 0] = np.linspace(0, 255, 256)  # Red channel
rgb_data[:, 2] = np.linspace(255, 0, 256)  # Blue channel

# Convert to a matplotlib colormap
custom_cmap = colormap_tools.uint8_rgb_arr2mpl_cmp(
    rgb_data,
    name="custom_blue_red",
    alpha=1.0,
    mode="linear"
)

# Use the custom colormap
plt.figure(figsize=(6, 6))
plt.imshow(data, cmap=custom_cmap)
plt.colorbar(label="Value")
plt.title("Custom Blue-Red Colormap")
plt.show()
```

## License

This project is licensed under the MIT license license.

## Contributing

Please follow the [Contributing Guide](./CONTRIBUTING.md) to contribute to this project.

## Contact

For support or inquiries, please contact:

- Email: info@meridianinno.com
