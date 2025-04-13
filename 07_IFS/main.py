# PRI0192
import random
import matplotlib.pyplot as plt
import numpy as np

class IFS:
    def __init__(self, model_mat: list[list[float]]):
        self.model = model_mat

    @staticmethod
    def __draw_graph(points):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        ax.scatter(xs, ys, zs)
        plt.show()

    def simulate(self, num_iterations: int):
        position = np.array([0.0, 0.0, 0.0])    # Starting position
        position_history = [position]           # All positions

        # Generate pos for each iteration
        for _ in range(num_iterations):
            # Choose random row
            r = random.choice(self.model)

            # Input values from random choice
            m = np.array([
                [r[0], r[1], r[2]],
                [r[3], r[4], r[5]],
                [r[6], r[7], r[8]],
            ])

            v = np.array([r[9], r[10], r[11]])

            # Affine transformation
            position = m @ position + v
            position_history.append(position)

        self.__draw_graph(position_history)

first_model = [
    [0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00],
    [-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00],
    [0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00]
]

second_model = [
    [0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.22, -0.45, 0.00, 1.00, 0.00],
    [-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00],
    [0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00]
]

if __name__ == '__main__':
    ifs_1 = IFS(first_model)
    ifs_2 = IFS(second_model)

    ifs_1.simulate(num_iterations=10000)
    ifs_2.simulate(num_iterations=10000)