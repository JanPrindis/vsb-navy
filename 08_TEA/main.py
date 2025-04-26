# PRI0192
from mandelbrot import *

print("========================================")
print("Click inside the plot to zoom in")
print("After closing the plot window a command to generate an animation will be shown")
print("========================================")

# Initial params
width, height = 600, 600
max_iter = 100

if cuda.is_available():
    width, height = 1000, 1000
    mex_iter = 500

zoom_scale = 0.5
total_zoom_factor = 1.0
colormap_name = None    # Or a matplotlib color colormap

# Initial bounds
aspect_ratio = width / height
x_min, x_max, y_min, y_max = compute_initial_bounds(aspect_ratio)

def redraw(center_x, center_y, zoom_scale):
    global x_min, x_max, y_min, y_max, total_zoom_factor

    x_min, x_max, y_min, y_max = zoom_to_center(
        np.float64(x_min), np.float64(x_max),
        np.float64(y_min), np.float64(y_max),
        zoom_scale, np.float64(center_x), np.float64(center_y)
    )
    total_zoom_factor *= zoom_scale

    if cuda.is_available():
        data = mandelbrot_set_gpu(
            np.float64(x_min), np.float64(x_max),
            np.float64(y_min), np.float64(y_max),
            width, height, max_iter
        )
    else:
        data = mandelbrot_set(
            np.float64(x_min), np.float64(x_max),
            np.float64(y_min), np.float64(y_max),
            width, height, max_iter
        )

    # Convert to color
    rgb_image = compute_colored_image(data.astype(np.float32), max_iter, colormap_name)

    ax.clear()
    ax.imshow(rgb_image, extent=[x_min, x_max, y_min, y_max], origin='lower', interpolation='nearest')
    ax.set_title(f"Zoom factor: {total_zoom_factor:.2e}", fontsize=10)
    fig.canvas.draw()

# On click event listener, that will zoom the plot
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f"[ZOOM]: {event.xdata} {event.ydata}")
        redraw(event.xdata, event.ydata, zoom_scale)

# Draw plot
fig, ax = plt.subplots()

if cuda.is_available():
    data = mandelbrot_set_gpu(x_min, x_max, y_min, y_max, width, height, max_iter)
else:
    data = mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter)

# Convert the raw data to color
rgb_image = compute_colored_image(data, max_iter, colormap_name)

# Draw
ax.imshow(rgb_image, extent=[x_min, x_max, y_min, y_max], origin='lower', interpolation='nearest')
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

# On exist calculate the centers
center_x = (x_min + x_max) / 2.0
center_y = (y_min + y_max) / 2.0

print("========================================")
print("To render a video, run this script:")
print(f"python create_video.py --center_x {center_x} --center_y {center_y} --zoom {total_zoom_factor:.2e}")
print("Or use create_video.py --help for more information")
print("========================================")
