# PRI0192
import random
from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

class Neighborhood(Enum):
    VON_NEUMANN = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    MOORE = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class Cell(Enum):
    EMPTY = 0
    TREE = 1
    BURNING = 2
    BURNT = 3

class ForestFire:
    def __init__(self, map_size: tuple[int, int], neighborhood: Neighborhood, title: str = "Forest Fire"):
        self.color_map = ListedColormap([
            "#522600",  # EMPTY
            "#009c00",  # TREE
            "#ff8000",  # BURNING
            "#000000"  # BURNT
        ])

        self.p = 0.05       # Regrowing probability
        self.f = 0.001      # Self-ignition probability
        self.density = 0.5  # Initial probability that cell will be a tree upon map generation

        self.neighborhood = neighborhood
        self.map_matrix = self.__generate_map(map_size)

        # Matplotlib setup
        self.fig, self.ax = plt.subplots()
        self.numeric_matrix = np.vectorize(lambda cell: cell.value)(self.map_matrix)
        self.img = self.ax.imshow(self.numeric_matrix, cmap=self.color_map, vmin=0, vmax=3)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title(title)

    def __generate_map(self, map_size):
        matrix = np.empty(map_size, dtype=Cell)
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if random.random() < self.density:
                    matrix[i][j] = Cell.TREE
                else:
                    matrix[i][j] = Cell.EMPTY
        return matrix

    def __tick(self):
        result = np.empty_like(self.map_matrix)
        shape = self.map_matrix.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                cell = self.map_matrix[i][j]

                # Empty cell
                if cell == Cell.EMPTY:
                    # Becomes tree with probability p
                    if random.random() < self.p:
                        result[i][j] = Cell.TREE
                    else:
                        result[i][j] = cell

                # Burnt cell becomes empty
                elif cell == Cell.BURNT:
                    result[i][j] = Cell.EMPTY

                # Burning cell becomes burnt
                elif cell == Cell.BURNING:
                    result[i][j] = Cell.BURNT

                # Tree cell
                elif cell == Cell.TREE:
                    is_neighbor_burning = False

                    for offset in self.neighborhood.value:
                        new_i = i + offset[0]
                        new_j = j + offset[1]

                        if new_i >= shape[0] or new_i < 0:
                            continue

                        if new_j >= shape[1] or new_j < 0:
                            continue

                        if self.map_matrix[new_i][new_j] == Cell.BURNING:
                            is_neighbor_burning = True
                            break

                    # Catches fire if neighbor is on fire
                    if is_neighbor_burning:
                        result[i][j] = Cell.BURNING
                    else:
                        # Or catches on fire by itself with probability f
                        if random.random() < self.f:
                            result[i][j] = Cell.BURNING
                        else:
                            result[i][j] = cell

        return result

    # Animation stuff
    def run(self, interval=100):
        def update_animation_frame(frame):
            self.map_matrix = self.__tick()
            self.numeric_matrix = np.vectorize(lambda cell: cell.value)(self.map_matrix)
            self.img.set_data(self.numeric_matrix)
            return [self.img]

        animation = FuncAnimation(self.fig, update_animation_frame, interval=interval, cache_frame_data=False)
        plt.show()


# Helper method for multithreading
def run_simulation(map_size, neighborhood, title):
    sim = ForestFire(map_size, neighborhood, title)
    sim.run()

if __name__ == '__main__':
    # Multithreading, so we can run them side by side
    from multiprocessing import Process
    from multiprocessing import set_start_method
    set_start_method('spawn')

    p1 = Process(target=run_simulation, args=((100, 100), Neighborhood.MOORE, "Moore"))
    p2 = Process(target=run_simulation, args=((100, 100), Neighborhood.VON_NEUMANN, "Von Neumann"))

    p1.start()
    p2.start()

    p1.join()
    p2.join()