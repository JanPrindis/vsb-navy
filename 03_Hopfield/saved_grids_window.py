import tkinter as tk

from grid_component import GridComponent
from matrix_component import MatrixComponent

class SaveWindow:
    def __init__(self, root, saved_patterns, grid_size=10):
        self.root = tk.Toplevel(root)
        self.root.title("Uložené grafy")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grid_size = grid_size
        self.saved_patterns = saved_patterns
        self.current_index = 0

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.prev_button = tk.Button(self.button_frame, text="<<", command=self.previous)
        self.prev_button.grid(row=0, column=0, padx=2)

        self.delete_button = tk.Button(self.button_frame, text="[DELETE]", command=self.delete_current)
        self.delete_button.grid(row=0, column=1, padx=2)

        self.next_button = tk.Button(self.button_frame, text=">>", command=self.next)
        self.next_button.grid(row=0, column=2, padx=2)

        self.toggle_view_button = tk.Button(self.button_frame, text="Show weights", command=self.toggle_view)
        self.toggle_view_button.grid(row=0, column=3, padx=2)

        # Content component
        self.grid_component = GridComponent(self.root, grid_size=grid_size, clickable=False)
        self.matrix_component = MatrixComponent(self.root, grid_size=grid_size * grid_size)

        self.showing_matrix = False

        self.update_content()

    def update_content(self):
        if self.saved_patterns:
            pattern = self.saved_patterns[self.current_index]
            # Update Grid
            self.grid_component.update_grid(pattern.pattern)

            # Update Matrix
            self.matrix_component.update_matrix(pattern.weight_matrix)

    def next(self):
        if self.saved_patterns and self.current_index < len(self.saved_patterns) - 1:
            self.current_index += 1
            self.update_content()

    def previous(self):
        if self.saved_patterns and self.current_index > 0:
            self.current_index -= 1
            self.update_content()

    def delete_current(self):
        if not self.saved_patterns:
            return

        del self.saved_patterns[self.current_index]

        if not self.saved_patterns:
            self.on_close()
            return

        self.current_index = min(self.current_index, len(self.saved_patterns) - 1)
        self.update_content()

    def toggle_view(self):
        if self.showing_matrix:
            self.matrix_component.hide()
            self.grid_component.show()
            self.toggle_view_button.config(text="Show weights")
        else:
            self.grid_component.hide()
            self.matrix_component.show()
            self.toggle_view_button.config(text="Show grid")

        self.showing_matrix = not self.showing_matrix

    def on_close(self):
        self.root.destroy()
