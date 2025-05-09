import numpy as np
import matplotlib.pyplot as plt


def generate_values(start: float, num: int):
    a_values = np.linspace(start, 4.0, num)
    values = []

    for a in a_values:
        x = 0.5

        for i in range(1000):
            x = a * x * (1 - x)

        for n in range(1000):
            x = a * x * (1 - x)
            values.append((a, x))

    return values


def draw_plot(values):
    x, y = zip(*values)
    plt.plot(x, y, ',k', alpha=.25)
    plt.show()


if __name__ == '__main__':
    draw_plot(generate_values(0, 1000))