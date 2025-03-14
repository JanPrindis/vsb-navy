# PRI0192
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import functools

class Perceptron:
    def __init__(self, func: callable):
        self.w_1 = 0.2
        self.w_2 = 0.4
        self.b = 0.5
        self.learning_rate = 0.1

        # Initialize the plot
        self.fig, self.ax = plt.subplots()
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.fig.canvas.mpl_connect(
            'button_press_event',
            functools.partial(self.__on_plot_click)
        )

        # Coords constraints
        self.x_constraints = (-10, 10)
        self.y_constraints = (-10, 10)

        self.func = func

    def __perceptron(self, x: float, y: float):
        guess = x * self.w_1 + y * self.w_2 + self.b
        if guess > 0:
            return 1
        if guess < 0:
            return -1
        return 0

    @staticmethod
    def __calculate_error(guess: int, expected: int):
        return expected - guess

    def __recalculate_weights(self, x: float, y:float, error: int):
        self.w_1 = self.w_1 + x * error * self.learning_rate
        self.w_2 = self.w_2 + y * error * self.learning_rate
        self.b = self.b + error * self.learning_rate

    def __evaluate_perceptron(self, x: float, y: float):
        perceptron_result = self.__perceptron(x, y)

        color = 'green'
        if perceptron_result == 1:
            color = 'red'
        elif perceptron_result == -1:
            color = 'blue'
        return color

    def train(self, n_samples: int):
        for i in range(n_samples):
            x = np.random.uniform(low=self.x_constraints[0], high=self.x_constraints[1], size=1)
            y = np.random.uniform(low=self.y_constraints[0], high=self.y_constraints[1], size=1)

            expected_result = 0         # On the line
            func_result = self.func(x)
            if func_result < y:
                expected_result = 1     # Above the line
            elif func_result > y:
                expected_result = -1    # Below the line

            # Get the result from the perceptron
            perceptron_result = self.__perceptron(x, y)
            # Calculate the error, and adjust weights
            self.__recalculate_weights(x, y, self.__calculate_error(perceptron_result, expected_result))

        print(f"After {n_samples} training cycles, the resulting weights are: w_1 = {self.w_1}, w_2 = {self.w_2}, b = {self.b}")

    def test(self, n_samples: int):
        # Plot the function line
        line_x = []
        line_y = []

        for i in range(10000):
            line_x.append(np.random.uniform(low=self.x_constraints[0], high=self.x_constraints[1], size=1))
            line_y.append(self.func(line_x[i]))

        self.ax.scatter(line_x, line_y, c="black", s=0.1)

        # Generate testing points
        x_coords = []
        y_coords = []
        colors = []

        for i in range(n_samples):
            x = np.random.uniform(low=self.x_constraints[0], high=self.x_constraints[1], size=1)
            y = np.random.uniform(low=self.y_constraints[0], high=self.y_constraints[1], size=1)

            x_coords.append(x)
            y_coords.append(y)

            colors.append(self.__evaluate_perceptron(x, y))

        self.ax.scatter(x_coords, y_coords, c=colors)
        self.ax.set(xlim = (self.x_constraints[0] * 1.2, self.x_constraints[1] * 1.2 ),
               ylim = (self.y_constraints[0] * 1.2, self.y_constraints[1] * 1.2 ))

        plt.show()

    def __on_plot_click(self, event):
        if event.button is MouseButton.LEFT and event.inaxes:
            x, y = event.xdata, event.ydata
            self.ax.scatter(x, y, c = self.__evaluate_perceptron(x, y))
            self.fig.canvas.draw_idle()

######################################################

def test_function(x: float):
    return 3 * x + 2

p = Perceptron(test_function)
p.train(n_samples=10000)
p.test(n_samples=100)
