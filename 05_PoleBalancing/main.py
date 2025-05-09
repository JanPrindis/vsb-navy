# PRI0192
import os.path
import random
import glob

import numpy as np

import pygame
import gymnasium as gym

class PoleBalancer:
    def __init__(self):
        self.alpha = 0.1     # Learning rate
        self.gamma = 0.99    # Discount factor
        self.epsilon = 0.1   # Epsilon-greedy param

        # Q-matrix definition
        self.n_actions = 2
        self.n_bins = 20
        self.max_velocity = 3.5    # Represents the Inf value

        self.Q, self.trained_iters = self.load_q_matrix()

        # Environment limits
        self.cart_position_bins = np.linspace(-4.8, 4.8, self.n_bins)
        self.cart_velocity_bins = np.linspace(-self.max_velocity, self.max_velocity, self.n_bins)
        self.pole_angle_bins = np.linspace(-0.418, 0.418, self.n_bins)
        self.pole_velocity_bins = np.linspace(-self.max_velocity, self.max_velocity, self.n_bins)

    # Split the values into discrete bins, so we can split them into states for Q-matrix
    def discretize(self, state):
        state_indices = [
            np.digitize(state[0], self.cart_position_bins) - 1, # Cart position
            np.digitize(state[1], self.cart_velocity_bins) - 1, # Cart velocity
            np.digitize(state[2], self.pole_angle_bins) - 1,    # Pole angle
            np.digitize(state[3], self.pole_velocity_bins) - 1  # Pole velocity
        ]
        return tuple(state_indices)


    def load_q_matrix(self):
        pattern = f"Q_{self.n_bins}_{self.n_actions}_*.npy"
        matches = glob.glob(pattern)

        def extract_iterations(filename):
            basename = os.path.basename(filename)
            parts = basename.replace(".npy", "").split("_")
            if len(parts) == 4:
                try:
                    return int(parts[3])
                except ValueError:
                    return -1
            return -1

        if matches:
            best_match = max(matches, key=extract_iterations)
            iterations = extract_iterations(best_match)
            print(f"Loading pre-trained Q-matrix from file {best_match}")
            return np.load(best_match), iterations
        else:
            print(f"Pre-trained Q-matrix not found {pattern}, creating new...")
            return np.zeros((self.n_bins, self.n_bins, self.n_bins, self.n_bins, self.n_actions)), 0

    def train(self, episodes: int):
        train_env = gym.make('CartPole-v1', render_mode=None)
        try:
            total_reward = 0

            for episode in range(episodes):
                state, _ = train_env.reset()
                state = self.discretize(state)
                death = False

                while not death:
                    # Epsilon-greedy approach
                    if random.uniform(0, 1) < self.epsilon:
                        action = train_env.action_space.sample()    # Random choice
                    else:
                        action = np.argmax(self.Q[state])           # Best choice from Q-matrix

                    # Get the next state
                    next_state, reward, death, _, _ = train_env.step(action)
                    next_state = self.discretize(next_state)

                    total_reward += reward

                    # Update Q-matrix
                    best_next_action = np.argmax(self.Q[next_state])
                    self.Q[state][action] = self.Q[state][action] + self.alpha * (reward + self.gamma * self.Q[next_state][best_next_action] - self.Q[state][action])

                    state = next_state

                self.trained_iters += 1

                if episode % 100 == 0:
                    print(f"Episode {episode}: average reward = {total_reward / 100}")
                    total_reward = 0

        except KeyboardInterrupt:
            print("Training interrupted")
        finally:
            np.save(f"Q_{self.n_bins}_{self.n_actions}_{self.trained_iters}.npy", self.Q)
            train_env.close()

    def test(self, max_attempts: int):
        test_env = gym.make('CartPole-v1', render_mode='human')
        try:
            state, _ = test_env.reset()
            state = self.discretize(state)
            total_reward = 0
            total_attempts = 0

            while True:
                action = np.argmax(self.Q[state])   # Just pick the best action from Q-matrix
                state, reward, death, _, _ = test_env.step(action)
                state = self.discretize(state)

                total_reward += reward

                # If death
                if death:
                    print(f"Resetting, gained reward: {total_reward}")
                    total_reward = 0

                    total_attempts += 1
                    if total_attempts >= max_attempts:
                        break

                    state, _ = test_env.reset()
                    state = self.discretize(state)

        except KeyboardInterrupt:
            pass
        finally:
            test_env.close()


if __name__ == "__main__":
    pb = PoleBalancer()

    # There should be a file containing pre-trained Q-matrix, so there is no need to train, but just in case...
    #pb.train(episodes=10000)

    # The pre-trained Q-mat seems to be too good, so 10 attempts might be an overkill
    pb.test(max_attempts=10)
