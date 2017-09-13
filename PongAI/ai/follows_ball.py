from PongAI.game import game
from PongAI.ai import ai


class FollowsBall(ai.AI):
    def __init__(self):
        pass

    def get_move(self, game_state):
        if game_state[0] > game_state[3]:
            return game.MovementDirection.Down
        else:
            return game.MovementDirection.Up
