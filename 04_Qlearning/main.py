# PRI0192
import tkinter as tk

from qlearning import QLearning
from grid_component import GridComponent
from matrix_component import MatrixComponent

class MainWindow:
    def __init__(self, root, grid_size=10, qLearning = None):
        self.grid_size = grid_size
        self.root = root
        self.root.title("Qlearning - PRI0192")

        self.qlearning = qLearning

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.find_button = tk.Button(self.button_frame, text="Find", command=self.find)
        self.find_button.grid(row=0, column=0, padx=2)

        self.learn_button = tk.Button(self.button_frame, text="Learn", command=self.learn)
        self.learn_button.grid(row=0, column=1, padx=2)

        self.toggle_block_button = tk.Button(self.button_frame, text="Selected block: BLANK", command=self.toggle_block)
        self.toggle_block_button.grid(row=0, column=2, padx=2)

        self.toggle_component_button = tk.Button(self.button_frame, text="View: MAP", command=self.toggle_view)
        self.toggle_component_button.grid(row=0, column=3, padx=2)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_grid)
        self.clear_button.grid(row=0, column=4, padx=2)

        # Content components
        self.component_id = 0
        self.components = [
            GridComponent(self.root, grid_size=grid_size, clickable=True, qLearning=self.qlearning),
            MatrixComponent(self.root, grid_size=grid_size * grid_size),
            MatrixComponent(self.root, grid_size=grid_size * grid_size)
        ]
        self.components_names = ["MAP", "ENV MATRIX", "AGENT MATRIX"]

        self.saved_patterns = []
        self.toggle_view(False)

    def toggle_view(self, switch=True):
        if switch:
            self.components[self.component_id].hide()
            self.component_id = (self.component_id + 1) % len(self.components)

        if self.component_id == 1:
            self.components[1].update_matrix(self.qlearning.env_matrix)

        self.components[self.component_id].show()
        self.toggle_component_button.config(text=f"View: {self.components_names[self.component_id]}")

    def find(self):
        def step():
            result = self.qlearning.next_step(self.components[0].get_matrix())
            self.components[0].update_grid(result[0])

            # It is the final step
            if result[1]:
                return

            self.root.after(200, step)

        step()

    def learn(self):
        self.qlearning.learn(1000)
        self.components[2].update_matrix(self.qlearning.agent_matrix)

    def toggle_block(self):
        self.toggle_block_button.config(text=f"Selected block: {self.components[0].toggle_block()}")

    def clear_grid(self):
        self.components[0].clear_grid()
        self.components[1].update_matrix(self.qlearning.env_matrix)
        self.components[2].update_matrix(self.qlearning.agent_matrix)

        self.qlearning.clear()


if __name__ == "__main__":
    grid_size = 7

    root = tk.Tk()
    app = MainWindow(
        root,
        grid_size=grid_size,
        qLearning=QLearning(
            grid_size=grid_size,
            learning_rate=0.8)
    )
    root.mainloop()
