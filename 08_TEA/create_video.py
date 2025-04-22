import shutil

import cv2
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import sys
from multiprocessing import freeze_support
from mandelbrot import *
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def zoom_to_center(xmin, xmax, ymin, ymax, zoom_factor, center_x, center_y):
    width = xmax - xmin
    height = ymax - ymin
    new_width = width * zoom_factor
    new_height = height * zoom_factor
    return (center_x - new_width / 2, center_x + new_width / 2,
            center_y - new_height / 2, center_y + new_height / 2)


def generate_frame(args):
    i, center_x, center_y, initial_bounds, zoom_factor, width, height, max_iter, num_frames = args
    z = zoom_factor ** (i / (num_frames - 1))
    xmin, xmax, ymin, ymax = zoom_to_center(*initial_bounds, z, center_x, center_y)
    data = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    hue = data / max_iter
    saturation = np.where(data == max_iter, 0, 1)
    value = np.where(data == max_iter, 0, 1)

    hsv_image = np.stack((hue, saturation, value), axis=-1)
    rgb_image = mcolors.hsv_to_rgb(hsv_image)

    data_uint8 = np.uint8(rgb_image * 255)
    return i, data_uint8

def generate_frame_hot_colormap(args):
    i, center_x, center_y, initial_bounds, zoom_factor, width, height, max_iter, num_frames = args
    z = zoom_factor ** (i / (num_frames - 1))
    xmin, xmax, ymin, ymax = zoom_to_center(*initial_bounds, z, center_x, center_y)
    data = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    normalized = data / max_iter

    colormap = plt.get_cmap('hot')
    colored = colormap(normalized)[:, :, :3]

    colored_uint8 = np.uint8(colored * 255)

    return i, colored_uint8

def main():
    width, height = 1920, 1080
    max_iter = 200
    #initial_bounds = (-2.0, 1.0, -1.5, 1.5)
    initial_bounds = (-2.0, 1.0, -0.84375, 0.84375)
    zoom_factor = 0.000000000001
    num_frames = 1440

    if len(sys.argv) != 3:
        sys.exit(1)

    center_x = float(sys.argv[1])
    center_y = float(sys.argv[2])

    os.makedirs("frames", exist_ok=True)

    print("Generating frames...")
    frames = []
    args_list = [(i, center_x, center_y, initial_bounds, zoom_factor, width, height, max_iter, num_frames)
                 for i in range(num_frames)]

    with ProcessPoolExecutor() as executor:
        for i, frame in tqdm(executor.map(generate_frame_hot_colormap, args_list), total=num_frames):
            path = f"frames/frame_{i:03d}.png"
            cv2.imwrite(path, frame)
            frames.append(path)

    print("Rendering video...")
    out = cv2.VideoWriter('zoom_animation_hot.mp4', -1, 24, (width, height))

    for path in frames:
        frame = cv2.imread(path)
        frame = cv2.flip(frame, 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()
    print("Finished rendering.")

    shutil.rmtree("frames")


if __name__ == "__main__":
    freeze_support()
    main()
