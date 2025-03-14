# PRI0192
import numpy as np

class SimpleNetwork:
    def __init__(self, seed: int):
        np.random.seed(seed)
        self.__w_h = np.random.randn(2, 2)  # Weights [w1, w2], [w3, w4]
        self.__b_h = np.random.randn(1, 2)  # Bias for hidden layer
        self.__w_o = np.random.randn(2, 1)  # Weights [w5, w6]
        self.__b_o = np.random.randn(1, 1)  # Bias for output layer


    def print_info(self):
        print("-----------------------------------------------------")
        print(f"Neuron hidden 1 weights\t{self.__w_h[0]}")
        print(f"Neuron hidden 2 weights\t{self.__w_h[1]}")
        print(f"Neuron output weights\t{self.__w_o[0]}")
        print(f"Neuron hidden 1 bias\t{self.__b_h[0][0]}")
        print(f"Neuron hidden 2 bias\t{self.__b_h[0][1]}")
        print(f"Neuron output bias\t\t{self.__b_o[0][0]}")
        print("-----------------------------------------------------")


    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))


    @staticmethod
    def __sigmoid_derivative(x):
        return x * (1 - x)


    def predict(self, x):
        # Hidden layer
        h_in = np.dot(x, self.__w_h) + self.__b_h
        h_out = self.__sigmoid(h_in)
        # Output layer
        f_in = np.dot(h_out, self.__w_o) + self.__b_o
        f_out = self.__sigmoid(f_in)
        return f_out


    def train(self, test_inputs: np.array, test_results : np.array, learning_rate: float, acceptable_error: float):
        print("-----------------------------------------------------")
        current_epoch = 0

        while True:
            current_epoch += 1

            # Forward
            hidden_input = np.dot(test_inputs, self.__w_h) + self.__b_h
            hidden_output = self.__sigmoid(hidden_input)

            final_input = np.dot(hidden_output, self.__w_o) + self.__b_o
            final_output = self.__sigmoid(final_input)

            # Total error calculation
            total_error = np.mean((test_results - final_output) ** 2)

            # Error backpropagation
            output_error = test_results - final_output
            output_delta = output_error * self.__sigmoid_derivative(final_output)

            hidden_error = np.dot(output_delta, self.__w_o.T)
            hidden_delta = hidden_error * self.__sigmoid_derivative(hidden_output)

            # Update weights
            self.__w_o += np.dot(hidden_output.T, output_delta) * learning_rate
            self.__b_o += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
            self.__w_h += np.dot(test_inputs.T, hidden_delta) * learning_rate
            self.__b_h += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

            # Print total error every 1000th epoch
            if current_epoch % 1000 == 0:
                print(f"Epoch {current_epoch}, Total error: {total_error:.4f}")

            # Is it good enough?
            if total_error < acceptable_error:
                print(f"Stopping training after {current_epoch} epochs, total error is {total_error:.4f}")
                print("-----------------------------------------------------")
                return


    def test(self, test_inputs: np.array, test_results : np.array):
        print("-----------------------------------------------------")
        print(" Input      | Expected | Guess      | Close Enough? ")
        print("-----------------------------------------------------")
        for i in range(len(test_inputs)):
            output = self.predict(test_inputs[i])
            is_close_enough = np.round(output) == test_results[i]

            input_str = f"{test_inputs[i]}"
            expected_str = f"{test_results[i][0]}"
            guess_str = f"{output[0][0]:.4f}"
            close_str = "True" if is_close_enough[0] else "False"

            print(f" {input_str:<10} | {expected_str:^8} | {guess_str:^10} | {close_str:^13} ")
        print("-----------------------------------------------------")


network = SimpleNetwork(seed=69)

print("Pre-training stats")
network.print_info()

print("Training")
local_testing_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
local_testing_results = np.array([[0], [1], [1], [0]])

network.train(
    test_inputs = local_testing_data,
    test_results = local_testing_results,
    learning_rate = 0.1,
    acceptable_error = 0.001
)

print("After-training stats")
network.print_info()

print("Testing...")
network.test(local_testing_data, local_testing_results)
