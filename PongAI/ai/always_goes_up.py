from PongAI.game import game
from PongAI.ai import ai


class AlwaysGoesUp(ai.AI):
    def __init__(self):
        pass

    def get_move(self, game_state):
        return game.MovementDirection.Up
