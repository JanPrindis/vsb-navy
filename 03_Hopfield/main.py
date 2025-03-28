# PRI0192
import tkinter as tk

from grid_component import GridComponent
from saved_grids_window import SaveWindow
from hopfield_network import HopfieldNetwork, Pattern

class MainWindow:
    def __init__(self, root, grid_size=10):
        self.grid_size = grid_size
        self.root = root
        self.root.title("Hopfield - PRI0192")

        self.save_window = None

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save pattern", command=self.save_pattern)
        self.save_button.grid(row=0, column=0, padx=2)

        self.repair_sync_button = tk.Button(self.button_frame, text="Repair pattern Sync", command=self.repair_pattern_sync)
        self.repair_sync_button.grid(row=0, column=1, padx=2)

        self.repair_async_button = tk.Button(self.button_frame, text="Repair pattern Async", command=self.repair_pattern_async)
        self.repair_async_button.grid(row=0, column=2, padx=2)

        self.show_patterns_button = tk.Button(self.button_frame, text="Show saved patterns", command=self.show_saved_patterns)
        self.show_patterns_button.grid(row=0, column=3, padx=2)

        self.clear_button = tk.Button(self.button_frame, text="Clear grid", command=self.clear_grid)
        self.clear_button.grid(row=0, column=4, padx=2)

        # Content component
        self.grid = GridComponent(self.root, grid_size=grid_size, clickable=True)

        self.saved_patterns = []

    def save_pattern(self):
        data = self.grid.get_matrix()
        self.saved_patterns.append(Pattern(data))

    def clear_grid(self):
        self.grid.clear_grid()

    def repair_pattern_sync(self):
        print("Repairing pattern synchronously...")
        weight_matrices = [pattern.weight_matrix for pattern in self.saved_patterns]
        fixed_matrix = HopfieldNetwork.synchronous_pattern_recovery(self.grid.get_matrix(), weight_matrices)
        self.grid.update_grid(fixed_matrix)

    def repair_pattern_async(self):
        print("Repairing pattern asynchronously...")
        weight_matrices = [pattern.weight_matrix for pattern in self.saved_patterns]
        fixed_matrix = HopfieldNetwork.asynchronous_pattern_recovery(self.grid.get_matrix(), weight_matrices)
        self.grid.update_grid(fixed_matrix)

    def show_saved_patterns(self):
        if not self.saved_patterns:
            print("No saved patterns found.")
            return

        if self.save_window is None or not self.save_window.root.winfo_exists():
            self.save_window = SaveWindow(self.root, self.saved_patterns, self.grid_size)
        else:
            self.save_window.root.lift()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root, grid_size=5)
    root.mainloop()
