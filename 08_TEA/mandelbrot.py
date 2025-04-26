# PRI0192

import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# ========================== CUDA IMPLEMENTATION ==========================
from numba import cuda

@cuda.jit
# Calculates a single pixels escape iteration, but faster
def mandelbrot_kernel(x_min, x_max, y_min, y_max, width, height, max_iter, result):
    x, y = cuda.grid(2)
    if x < width and y < height:
        # Calculate the complex number form current position in grid
        real = x_min + (x_max - x_min) * x / width
        imag = y_min + (y_max - y_min) * y / height
        c = complex(real, imag)

        z = 0j
        for n in range(max_iter):
            if abs(z) > 2:
                result[y, x] = n
                return
            z = z * z + c

        result[y, x] = max_iter

# Calculates an 2D array of escape iterations, but faster
def mandelbrot_set_gpu(x_min, x_max, y_min, y_max, width, height, max_iter):
    # Result matrix
    result = np.empty((height, width), dtype=np.float64)
    result_device = cuda.to_device(result)

    # CUDA kernel definition
    threads_per_block = (32, 32)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # CUDA run
    mandelbrot_kernel[blocks_per_grid, threads_per_block](
        x_min, x_max, y_min, y_max, width, height, max_iter, result_device
    )

    result = result_device.copy_to_host()
    return result
# ========================================================================

# ========================== CPU IMPLEMENTATION ==========================
# Calculates a single pixels escape iteration
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


# Calculates an 2D array of escape iterations
def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    result = np.empty((height, width), dtype=np.float64)
    for i in range(height):
        for j in range(width):
            c = complex(real[j], imag[i])
            result[i, j] = mandelbrot(c, max_iter)
    return result
# =======================================================================


# Uses the escape iteration as hue value
def compute_hsv_coloring(data, max_iter):
    hue = data / max_iter
    saturation = np.where(data == max_iter, 0, 1)
    value = np.where(data == max_iter, 0, 1)
    hsv_image = np.stack((hue, saturation, value), axis=-1)
    rgb_image = mcolors.hsv_to_rgb(hsv_image)
    return rgb_image


# Compute the frames colors
def compute_colored_image(data, max_iter, colormap_name=None):
    if colormap_name is None:
        return compute_hsv_coloring(data, max_iter)
    else:
        normalized = data / max_iter
        cmap = plt.colormaps.get_cmap(colormap_name)
        colored = cmap(normalized)[:, :, :3]  # Ignore alpha channel
        return colored


def zoom_to_center(x_min, x_max, y_min, y_max, zoom_factor, center_x, center_y):
    width = x_max - x_min
    height = y_max - y_min
    new_width = width * zoom_factor
    new_height = height * zoom_factor
    return (center_x - new_width / 2, center_x + new_width / 2,
            center_y - new_height / 2, center_y + new_height / 2)


# Recalculates the initial bounds based on output resolution
def compute_initial_bounds(aspect_ratio):
    default_width = 3.0
    default_height = 3.0

    if aspect_ratio >= 1:
        width = default_width       # Wider
        height = width / aspect_ratio
    else:
        height = default_height     # Taller
        width = height * aspect_ratio

    center_x = (-2.0 + 1.0) / 2
    center_y = (-1.5 + 1.5) / 2

    x_min = center_x - width / 2
    x_max = center_x + width / 2
    y_min = center_y - height / 2
    y_max = center_y + height / 2

    return x_min, x_max, y_min, y_max