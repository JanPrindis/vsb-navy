import numpy as np
import matplotlib.pyplot as plt
from mandelbrot import *
import matplotlib.colors as mcolors

xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5
width, height = 800, 600
max_iter = 100
zoom_factor = 0.5


def redraw(center_x, center_y, zoom_scale):
    global xmin, xmax, ymin, ymax
    width_range = (xmax - xmin) * zoom_scale
    height_range = (ymax - ymin) * zoom_scale
    xmin = center_x - width_range / 2
    xmax = center_x + width_range / 2
    ymin = center_y - height_range / 2
    ymax = center_y + height_range / 2

    result = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    normed_result = result / max_iter

    hue = normed_result
    saturation = np.where(result == max_iter, 0, 1)
    value = np.where(result == max_iter, 0, 1)

    hsv_image = np.stack((hue, saturation, value), axis=-1)
    rgb_image = mcolors.hsv_to_rgb(hsv_image)

    ax.clear()
    ax.imshow(rgb_image, extent=[xmin, xmax, ymin, ymax], origin='lower')
    fig.canvas.draw()


def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f"[ZOOM]: {event.xdata} {event.ydata}")
        redraw(event.xdata, event.ydata, zoom_factor)


fig, ax = plt.subplots()
result = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

normed_result = result / max_iter

hue = normed_result
saturation = np.where(result == max_iter, 0, 1)
value = np.where(result == max_iter, 0, 1)

hsv_image = np.stack((hue, saturation, value), axis=-1)
rgb_image = mcolors.hsv_to_rgb(hsv_image)

ax.imshow(rgb_image, extent=[xmin, xmax, ymin, ymax], origin='lower')
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

center_x = (xmin + xmax) / 2.0
center_y = (ymin + ymax) / 2.0
print(f"Center X: {center_x}, Center Y: {center_y}")
