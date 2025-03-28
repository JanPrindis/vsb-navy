import tkinter as tk

class MatrixComponent:
    def __init__(self, parent, grid_size):
        self.frame = tk.Frame(parent)
        self.grid_size = grid_size
        self.labels = [[tk.Label(self.frame, text="0", width=4, height=2, borderwidth=1, relief="solid")
                        for _ in range(grid_size)] for _ in range(grid_size)]

        for i in range(grid_size):
            for j in range(grid_size):
                self.labels[i][j].grid(row=i, column=j, padx=1, pady=1)

    def update_matrix(self, matrix):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.labels[i][j].config(text=str(matrix[i][j]))

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()