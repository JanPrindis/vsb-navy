import numpy as np

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    result = np.empty((height, width))
    for i in range(height):
        for j in range(width):
            c = complex(real[j], imag[i])
            result[i, j] = mandelbrot(c, max_iter)
    return result