import random
import numpy as np

from enums import *

class QLearning:
    def __init__(self, grid_size, learning_rate):
        self.grid_size = grid_size
        self.mat_size = grid_size * grid_size

        # R-matrix
        self.env_matrix = np.full((self.mat_size * self.mat_size, self.mat_size * self.mat_size), -1)

        # Q-matrix
        self.agent_matrix = np.full((self.mat_size * self.mat_size, self.mat_size * self.mat_size), 0)

        self.agent_pos = None

        # Stats
        self.total_found = 0
        self.total_died = 0
        self.total_episodes = 0

        # Learning rate
        self.gamma = learning_rate

        self.success_score = 100
        self.penalty_score = -100

    def __find_agent_pos(self, map_matrix: np.ndarray):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if map_matrix[i, j] == Type.MOUSE.value:
                    return i, j

        return None

    def __position_to_index(self, row, col):
        return row * self.grid_size + col

    def __index_to_position(self, index):
        row = index // self.grid_size
        col = index % self.grid_size
        return row, col

    def calculate_env_matrix(self, map_matrix: np.ndarray):
        self.env_matrix.fill(-1)
        self.agent_matrix.fill(0)
        self.agent_pos = self.__find_agent_pos(map_matrix)

        if self.agent_pos is None:
            print("Warning, Agent not found.")

        def is_accessible(row, col):
            return map_matrix[row, col] != Type.WALL.value

        # Helper function that propagates the current value to neighbors
        def update_env_matrix_for_neighbors(row, col, current_index):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.grid_size and 0 <= new_col < self.grid_size:
                    neighbor_index = self.__position_to_index(new_row, new_col)

                    if map_matrix[new_row, new_col] == Type.CHEESE.value:
                        self.env_matrix[current_index, neighbor_index] = self.success_score

                    elif map_matrix[new_row, new_col] == Type.TRAP.value:
                        self.env_matrix[current_index, neighbor_index] = self.penalty_score

                    elif is_accessible(new_row, new_col):
                        self.env_matrix[current_index, neighbor_index] = 0

        # Loop through the map
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                current_index = self.__position_to_index(row, col)

                if map_matrix[row, col] == Type.CHEESE.value:
                    self.env_matrix[current_index, current_index] = self.success_score
                    update_env_matrix_for_neighbors(row, col, current_index)

                elif map_matrix[row, col] == Type.TRAP.value:
                    self.env_matrix[current_index, current_index] = self.penalty_score

                elif is_accessible(row, col):
                    update_env_matrix_for_neighbors(row, col, current_index)

                else:
                    self.env_matrix[current_index, current_index] = -1 # Wall

    def learn(self, episodes=100):
        if self.agent_pos is None:
            print("Error, Agent not found.")
            return

        for episode in range(episodes):
            current_pos = self.__position_to_index(self.agent_pos[0], self.agent_pos[1])

            while True:
                # Randomly choose next step
                actions = [i for i in range(self.env_matrix.shape[1]) if self.env_matrix[current_pos, i] != -1]
                next_pos = random.choice(actions)

                # Calculate q-matrix value for this step
                reward = self.env_matrix[current_pos, next_pos]
                self.agent_matrix[current_pos, next_pos] = reward + self.gamma * np.max(self.agent_matrix[next_pos])

                # Found goal
                if reward == 100:
                    self.total_found += 1
                    break

                # Died
                if reward == -100:
                    self.total_died += 1
                    break

                current_pos = next_pos

        self.total_episodes += episodes

        print(f"After {self.total_episodes} learning episodes.")
        print(f"Agent found goal {self.total_found}x")
        print(f"Agent died {self.total_died}x")
        pass

    def next_step(self, current_state: np.ndarray):
        # Get all available options from the Q-matrix
        options = self.agent_matrix[self.__position_to_index(self.agent_pos[0], self.agent_pos[1])]

        # Check if the best path has propagated to current pos
        if max(options) == 0:
            print("Not enough information to decide next action.")
            return current_state, True

        # Redraw agent
        current_state[self.agent_pos[0], self.agent_pos[1]] = Type.EMPTY.value

        # Pick the best path
        next_action = np.argmax(options)
        self.agent_pos = self.__index_to_position(next_action)

        # Check if move is even valid
        if (current_state[self.agent_pos[0], self.agent_pos[1]] == Type.WALL.value or
            current_state[self.agent_pos[0], self.agent_pos[1]] == Type.TRAP.value):
            print("Agent has died trying to reach the goal")

            return current_state, True

        # Check if agent has reached the goal
        if current_state[self.agent_pos[0], self.agent_pos[1]] == Type.CHEESE.value:
            print("Agent has reached the goal")
            current_state[self.agent_pos[0], self.agent_pos[1]] = Type.MOUSE.value

            return current_state, True

        # Return new state
        current_state[self.agent_pos[0], self.agent_pos[1]] = Type.MOUSE.value
        return current_state, False

    def clear(self):
        self.env_matrix = np.full((self.mat_size * self.mat_size, self.mat_size * self.mat_size), -1)
        self.agent_matrix = np.full((self.mat_size * self.mat_size, self.mat_size * self.mat_size), 0)
        self.agent_pos = None

        self.total_found = 0
        self.total_died = 0
        self.total_episodes = 0

