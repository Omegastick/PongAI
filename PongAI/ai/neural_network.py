from PongAI.game import game
from PongAI.ai import ai
import numpy as np


class NeuralNetwork(ai.AI):
    """Neural network based pong AI. Initialises with random synapses"""

    def __init__(self):
        # Synapses
        self.syn0 = 2 * np.random.random((4, 4)) - 1
        self.syn1 = 2 * np.random.random((4, 8)) - 1
        self.syn2 = 2 * np.random.random((8, 2)) - 1

    def get_move(self, game_state):
        # Layers
        l0 = np.array(game_state)
        l1 = self._nonlin(np.dot(l0, self.syn0))
        l2 = self._nonlin(np.dot(l1, self.syn1))
        l3 = self._nonlin(np.dot(l2, self.syn2))

        if l3[0] > l3[1]:
            return game.MovementDirection.Up
        else:
            return game.MovementDirection.Down

    def _nonlin(self, x):
        """Sigmoid function"""
        return 1 / (1 + np.exp(-x))
