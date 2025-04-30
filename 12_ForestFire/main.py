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


color_map = ListedColormap([
    "#522600",  # EMPTY
    "#009c00",  # TREE
    "#ff8000",  # BURNING
    "#000000"  # BURNT
])


p = 0.05
f = 0.001
density = 0.5


def generate_map(map_size):
    map_matrix = np.empty(map_size, dtype=Cell)
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if random.random() < density:
                map_matrix[i][j] = Cell.TREE
            else:
                map_matrix[i][j] = Cell.EMPTY

    return map_matrix


def update(frame):
    global map_matrix
    map_matrix = tick(map_matrix, Neighborhood.MOORE)

    numeric_matrix = np.vectorize(lambda cell: cell.value)(map_matrix)
    img.set_data(numeric_matrix)

    return [img]


def tick(map_matrix, neighborhood: Neighborhood):
    result = np.empty_like(map_matrix)
    shape = map_matrix.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            cell = map_matrix[i][j]

            if cell == Cell.EMPTY:
                if random.random() < p:
                    result[i][j] = Cell.TREE
                else:
                    result[i][j] = cell

            elif cell == Cell.BURNT:
                result[i][j] = Cell.EMPTY

            elif cell == Cell.BURNING:
                result[i][j] = Cell.BURNT

            elif cell == Cell.TREE:
                is_neighbor_burning = False

                for offset in neighborhood.value:
                    new_i = i + offset[0]
                    new_j = j + offset[1]

                    if new_i >= shape[0] or new_i < 0:
                        continue

                    if new_j >= shape[1] or new_j < 0:
                        continue

                    if map_matrix[new_i][new_j] == Cell.BURNING:
                        is_neighbor_burning = True
                        break

                if is_neighbor_burning:
                    result[i][j] = Cell.BURNING
                else:
                    if random.random() < f:
                        result[i][j] = Cell.BURNING
                    else:
                        result[i][j] = cell

    return result

if __name__ == '__main__':
    map_matrix = generate_map((100, 100))

    fig, ax = plt.subplots()
    numeric_matrix = np.vectorize(lambda cell: cell.value)(map_matrix)

    img = ax.imshow(numeric_matrix, cmap=color_map, vmin=0, vmax=3)
    ax.set_xticks([])
    ax.set_yticks([])


    animation = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    plt.show()