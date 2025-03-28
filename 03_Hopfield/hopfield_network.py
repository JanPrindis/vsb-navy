import numpy
import numpy as np

class HopfieldNetwork:
    @staticmethod
    def calculate_weight_matrix(input_matrix: numpy.ndarray) -> numpy.ndarray:
        input_vector = input_matrix.reshape(-1, 1)

        # Replace 0 with -1
        input_vector[input_vector == 0] = -1

        # Weight matrix calculation
        weight_matrix = input_vector @ input_vector.T
        np.fill_diagonal(weight_matrix, 0)
        return weight_matrix

    @staticmethod
    def asynchronous_pattern_recovery(input_pattern: numpy.ndarray, weights: list[numpy.ndarray]) -> numpy.ndarray:
        # Weight matrices are passed separately, they are added together here
        weight_matrix = sum(weights)

        # Squish and replace 0 with -1
        fixed_pattern = input_pattern.reshape(-1, 1)
        fixed_pattern[fixed_pattern == 0] = -1

        # Activate neurons
        for i in range(fixed_pattern.shape[0]):
            weighted_sum = weight_matrix[i, :] @ fixed_pattern
            fixed_pattern[i] = 1 if weighted_sum >= 0 else -1 # "Sign function"

        # Replace -1 back to 0
        fixed_pattern[fixed_pattern == -1] = 0
        return fixed_pattern.reshape(input_pattern.shape)

    @staticmethod
    def synchronous_pattern_recovery(input_pattern: numpy.ndarray, weights: list[numpy.ndarray]) -> numpy.ndarray:
        # Weight matrices are passed separately, they are added together here
        weight_matrix = sum(weights)

        # Squish and replace 0 with -1
        fixed_pattern = input_pattern.reshape(-1, 1)
        fixed_pattern[fixed_pattern == 0] = -1

        # All at once
        weighted_sums = weight_matrix @ fixed_pattern
        fixed_pattern = np.where(weighted_sums >= 0, 1, -1)

        # Replace -1 back to 0
        fixed_pattern[fixed_pattern == -1] = 0
        return fixed_pattern.reshape(input_pattern.shape)

class Pattern:
    def __init__(self, pattern: numpy.ndarray):
        self.pattern = pattern
        self.weight_matrix = HopfieldNetwork.calculate_weight_matrix(self.pattern)
