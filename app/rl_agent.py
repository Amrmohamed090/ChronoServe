import random

class RLAgent:
    def __init__(self):
        self.q_table = {}  # (endpoint, backend) -> reward
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2  # exploration rate

    def choose_backend(self, endpoint, available_backends):
        if random.random() < self.epsilon:
            return random.choice(available_backends)
        q_values = {b: self.q_table.get((endpoint, b), 0) for b in available_backends}
        return max(q_values, key=q_values.get)

    def update(self, endpoint, backend, reward):
        old_value = self.q_table.get((endpoint, backend), 0)
        new_value = old_value + self.alpha * (reward - old_value)
        self.q_table[(endpoint, backend)] = new_value
