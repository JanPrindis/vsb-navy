# PRI0192

import shutil
import cv2
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
from mandelbrot import *
import argparse

# Generates a single frame
def generate_frame(args):
    (i, center_x, center_y, initial_bounds, zoom_factor,
     width, height, max_iter, num_frames, colormap_name) = args

    z = zoom_factor ** (i / (num_frames - 1))
    x_min, x_max, y_min, y_max = zoom_to_center(*initial_bounds, z, center_x, center_y)

    if cuda.is_available():
        data = mandelbrot_set_gpu(x_min, x_max, y_min, y_max, width, height, max_iter)
    else:
        data = mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter)

    rgb_image = compute_colored_image(data, max_iter, colormap_name)
    frame = np.uint8(rgb_image * 255)

    return i, frame


def main():
    parser = argparse.ArgumentParser(description="Generate Mandelbrot zoom animation")
    parser.add_argument('--width', type=int, default=1920, help='Video width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Video height (default: 1080)')
    parser.add_argument('--max_iter', type=int, default=200, help='Max iterations until escape (default: 200)')
    parser.add_argument('--zoom', type=float, default=1e-12, help='Target zoom factor (default: 1e-12)')
    parser.add_argument('--frames', type=int, default=140, help='Number of frames (default: 140) = 10 seconds @ 24fps')
    parser.add_argument('--colormap', type=str, default=None, help='Matplotlib colormap (or None for HSV coloring)')
    parser.add_argument('--center_x', type=float, required=True, help='Zoom center X coordinate')
    parser.add_argument('--center_y', type=float, required=True, help='Zoom center Y coordinate')

    args = parser.parse_args()

    width = args.width
    height = args.height
    max_iter = args.max_iter
    zoom_factor = args.zoom
    num_frames = args.frames
    colormap_name = args.colormap
    center_x = args.center_x
    center_y = args.center_y

    aspect_ratio = width / height
    initial_bounds = compute_initial_bounds(aspect_ratio)

    os.makedirs("frames", exist_ok=True)

    print("Generating frames...")
    frames = []
    args_list = [(i, center_x, center_y, initial_bounds, zoom_factor,
                  width, height, max_iter, num_frames, colormap_name)
                 for i in range(num_frames)]

    if cuda.is_available():
        # GPU is used
        for args in tqdm(args_list, total=num_frames):
            i, frame = generate_frame(args)
            path = f"frames/frame_{i:04d}.png"
            cv2.imwrite(path, frame)
            frames.append(path)

    else:
        # Frames are calculated on separate threads
        with ProcessPoolExecutor() as executor:
            for i, frame in tqdm(executor.map(generate_frame, args_list), total=num_frames):
                path = f"frames/frame_{i:04d}.png"
                cv2.imwrite(path, frame)
                frames.append(path)

    print("Rendering video...")
    out = cv2.VideoWriter('zoom_animation.mp4', -1, 24, (width, height))

    for path in frames:
        frame = cv2.imread(path)
        frame = cv2.flip(frame, 0)              # Vertical flip cuz OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # RGB -> BGR cuz more OpenCV shenanigans
        out.write(frame)

    out.release()
    print("Finished rendering.")

    # Cleanup
    shutil.rmtree("frames")

if __name__ == "__main__":
    freeze_support()
    main()
