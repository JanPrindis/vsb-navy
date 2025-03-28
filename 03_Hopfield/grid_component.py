import tkinter as tk
import numpy as np
from functools import partial

class GridComponent:
    def __init__(self, parent, grid_size=10, clickable=True):
        self.grid_size = grid_size
        self.clickable = clickable
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10)

        self.grid_matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)

        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                button = tk.Button(self.frame, width=4, height=2, bg="white")
                button.grid(row=i, column=j, padx=0, pady=0)

                if self.clickable:
                    button.config(command=partial(self.toggle_button, i, j))

                self.buttons[i][j] = button

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def update_grid(self, matrix):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "black" if matrix[i, j] == 1 else "white"
                self.buttons[i][j].config(bg=color)

    def toggle_button(self, i, j):
        button = self.grid_matrix[i][j]
        if button == 0:
            self.grid_matrix[i][j] = 1
            self.buttons[i][j].config(bg="black")
        else:
            self.grid_matrix[i][j] = 0
            self.buttons[i][j].config(bg="white")

    def clear_grid(self):
        self.grid_matrix.fill(0)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].config(bg="white")

    def get_matrix(self):
        return self.grid_matrix.copy()