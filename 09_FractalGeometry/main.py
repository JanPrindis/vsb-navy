# PRI0192

import copy
import random
import tkinter as tk
from tkinter import colorchooser

class FractalGeometry:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Terrain")
        self.root.geometry("1000x600")
        self.picked_color = "#FF0000"

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(self.main_frame, width=1000, height=600)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=200, padx=10, pady=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.startPosX_entry = self.add_labeled_entry(self.control_frame, "Start Pos X", 0)
        self.startPosY_entry = self.add_labeled_entry(self.control_frame, "Start Pos Y", 300)
        self.endPosX_entry = self.add_labeled_entry(self.control_frame, "End Pos X", 1000)
        self.endPosY_entry = self.add_labeled_entry(self.control_frame, "End Pos Y", 369)
        self.numIter_entry = self.add_labeled_entry(self.control_frame, "Num of iterations", 5)
        self.heightOffset_entry = self.add_labeled_entry(self.control_frame, "Height offset", 10)

        self.color_button = tk.Button(self.control_frame, command=self.pick_color)
        self.set_button_color(self.picked_color)
        self.color_button.pack(pady=5)

        self.draw_button = tk.Button(self.control_frame, text="Draw", command=self.draw)
        self.draw_button.pack(pady=5)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear)
        self.clear_button.pack(pady=5)


    # Helper method for creating inputs
    @staticmethod
    def add_labeled_entry(parent, label_text, initial_value=None):
        label = tk.Label(parent, text=label_text)
        label.pack()
        entry = tk.Entry(parent)

        if initial_value:
            entry.insert(0, initial_value)

        entry.pack()
        return entry

    # Helper methods for parsing number inputs
    @staticmethod
    def set_default_int(var):
        if var == '':
            return 0
        else:
            return int(var)

    @staticmethod
    def set_default_float(var):
        if var == '':
            return 0.0
        else:
            return float(var)

    # Helper method for updating color picker buttons color
    def set_button_color(self, color):
        self.color_button.config(
            bg=color,
            activebackground=color,
            relief=tk.FLAT,
            padx=55,
            pady=0,
            borderwidth=2,
            highlightthickness=1,
        )

    # Color picker
    def pick_color(self):
        color = colorchooser.askcolor(title="Terrain color")[1]
        if color:
            print(f"Picked color {color}")
            self.picked_color = color
            self.set_button_color(color)

    @staticmethod
    # Custom iterator, that returns tuples
    def moving_window(n, iterable):
        start, stop = 0, n
        while stop <= len(iterable):
            yield iterable[start:stop]
            start += 1
            stop += 1

    def draw(self):
        # Set default values if variables not set (0)
        start_x = self.set_default_float(self.startPosX_entry.get())
        start_y = self.set_default_float(self.startPosY_entry.get())
        end_x = self.set_default_float(self.endPosX_entry.get())
        end_y = self.set_default_float(self.endPosY_entry.get())
        n_iter = self.set_default_int(self.numIter_entry.get())
        offset = self.set_default_float(self.heightOffset_entry.get())

        splits = [(start_x, start_y), (end_x, end_y)]

        # Iterations
        for i in range(n_iter):
            new_splits = [splits[0]]

            # For each tuple
            for x in self.moving_window(2, splits):
                begin = x[0]
                end = x[1]

                # Split in the middle
                new_split_x = (begin[0] + end[0]) / 2
                new_split_y = (begin[1] + end[1]) / 2

                # 50% change of offsetting above or below
                if random.random() < 0.5:
                    new_split_y += offset
                else:
                    new_split_y -= offset

                # Add new point with vertical offset
                new_splits.append((new_split_x, new_split_y))
                new_splits.append(end)

            splits = copy.deepcopy(new_splits)

        # Add bottom edges
        height_of_polygon = 600 # A made up number (tm)
        splits.append((splits[-1][0], height_of_polygon))
        splits.append((splits[0][0], height_of_polygon))

        # Draw as polygon
        flattened = [a for x in splits for a in x]
        self.canvas.create_polygon(*flattened, fill=self.picked_color, outline="")

    def clear(self):
        self.canvas.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = FractalGeometry(root)
    root.mainloop()