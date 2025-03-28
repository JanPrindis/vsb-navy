import tkinter as tk
import numpy as np
from functools import partial
from PIL import Image, ImageTk

from enums import *

class GridComponent:
    def __init__(self, parent, grid_size=10, clickable=True, qLearning=None):
        self.grid_size = grid_size
        self.clickable = clickable
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10)
        self.active_type = Type.EMPTY
        self.qlearning = qLearning

        self.images = {}

        self.grid_matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)

        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                button = tk.Button(self.frame, width=4, height=2, bg="white")
                button.grid(row=i, column=j, padx=0, pady=0)

                if self.clickable:
                    button.config(command=partial(self.toggle_button, i, j))

                self.buttons[i][j] = button

        parent.after(100, self.load_images)

    def load_images(self):
        button = self.buttons[0][0]
        button.update_idletasks()

        # NENAVIDIM TKINTER, NENAVIDIM TKINTER, NENAVIDIM TKINTER, NENAVIDIM TKINTER, NENAVIDIM TKINTER
        self.button_width = button.winfo_width() - 6
        self.button_height = button.winfo_height() - 6

        self.images = {
            Type.MOUSE: self.load_and_resize_image("./img/mouse.png"),
            Type.WALL: self.load_and_resize_image("./img/wall.png"),
            Type.TRAP: self.load_and_resize_image("./img/trap.png"),
            Type.CHEESE: self.load_and_resize_image("./img/cheese.png"),
        }

    def load_and_resize_image(self, path):
        image = Image.open(path)
        image = image.resize((self.button_width, self.button_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def toggle_button(self, i, j, forced_type = None):
        if forced_type is None:
            forced_type = self.active_type

        if forced_type is not None and forced_type != Type.EMPTY:

            # Only single goal/agent is allowed
            if forced_type == Type.MOUSE or forced_type == Type.CHEESE:
                self.delete_type(forced_type)

            self.grid_matrix[i][j] = self.active_type.value
            self.buttons[i][j].config(
                image=self.images[self.active_type],
                bg="white",
                compound="center"
            )
            self.buttons[i][j].image = self.images[self.active_type]
            self.buttons[i][j].config(width=self.button_width, height=self.button_height)
        else:
            self.buttons[i][j].config(image="", bg="white")
            self.buttons[i][j].config(width=4, height=2)
            self.grid_matrix[i][j] = Type.EMPTY.value

        self.qlearning.calculate_env_matrix(self.grid_matrix.copy())


    def clear_grid(self):
        self.grid_matrix.fill(0)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].config(image="", bg="white")
                self.buttons[i][j].config(width=4, height=2)


    def get_matrix(self):
        return self.grid_matrix.copy()

    def toggle_block(self):
        selected_index = (self.active_type.value + 1) % len(Type)
        self.active_type = Type(selected_index)
        return self.active_type.name

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def delete_type(self, searched_type: Type):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid_matrix[i][j] == searched_type.value:
                    self.toggle_button(i, j, Type.EMPTY)

    def update_grid(self, matrix):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = matrix[i][j]
                if value != Type.EMPTY.value:
                    self.grid_matrix[i][j] = value
                    self.buttons[i][j].config(
                        image=self.images[Type(value)],
                        bg="white",
                        compound="center"
                    )
                    self.buttons[i][j].image = self.images[Type(value)]
                    self.buttons[i][j].config(width=self.button_width, height=self.button_height)
                else:
                    self.buttons[i][j].config(image="", bg="white")
                    self.buttons[i][j].config(width=4, height=2)
                    self.grid_matrix[i][j] = Type.EMPTY.value