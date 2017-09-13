from PongAI.game import game
from PongAI.ai import ai
import random


class RandomDirection(ai.AI):
    def __init__(self):
        pass

    def get_move(self, game_state):
        if random.randint(0, 1):
            return game.MovementDirection.Up
        else:
            return game.MovementDirection.Down
