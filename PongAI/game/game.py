from enum import Enum
import random



class Players(Enum):
    """Enum for players"""
    Left, Right = range(2)


class MovementDirection(Enum):
    """Enum for possible movement directions"""
    Up, Down = range(2)


class PongGame:
    """Model and logic for a game of pong"""
    def __init__(self, left_ai, right_ai, generation):
        self.ball_x = 50
        self.ball_y = 50
        if random.randint(0, 1):
            self.ball_direction = 1
        else:
            self.ball_direction = -1
        self.left_paddle_location = 50
        self.right_paddle_location = 50

        self.ball_speed = 1
        self.ball_vertical_speed = 0.61
        if random.randint(0, 1):
            self.ball_vertical_speed = -self.ball_vertical_speed
        self.paddle_speed = 0.5
        self.paddle_size = 20

        self.left_ai = left_ai
        self.right_ai = right_ai

        self.generation = generation

        self.fast = True

        self.length = 0

    def state(self, active_player):
        """Returns the current state of the game in a tuple of form:
        (ball_y, ball_distance, ball_direction, paddle_location)"""
        if active_player == Players.Left:
            ball_distance = float(self.ball_y)
            ball_direction = self.ball_direction
            paddle_location = float(self.left_paddle_location)
        elif active_player == Players.Right:
            ball_distance = (100 - float(self.ball_y))
            ball_direction = self.ball_direction * -1
            paddle_location = float(self.right_paddle_location)

        return (float(self.ball_y) / 100, ball_distance / 100, ball_direction, paddle_location / 100)

    def move(self, paddle_to_move, direction):
        """Moves one of the paddles"""
        if paddle_to_move == Players.Left:
            if direction == MovementDirection.Up:
                self.left_paddle_location -= self.paddle_speed
            elif direction == MovementDirection.Down:
                self.left_paddle_location += self.paddle_speed
        elif paddle_to_move == Players.Right:
            if direction == MovementDirection.Up:
                self.right_paddle_location -= self.paddle_speed
            elif direction == MovementDirection.Down:
                self.right_paddle_location += self.paddle_speed

    def update(self):
        """Moves the ball, assesses whether someone has won or not. Returns the winner"""
        self.length += 1
        self.ball_y += self.ball_vertical_speed
        self.ball_x += self.ball_direction * self.ball_speed

        if self.ball_y >= 100 or self.ball_y <= 0:
            self.ball_vertical_speed = self.ball_vertical_speed * -1

        if self.ball_x >= 100:
            if abs(self.right_paddle_location - self.ball_y) <= self.paddle_size:
                self.ball_direction = self.ball_direction * -1
            else:
                return Players.Left

        if self.ball_x <= 0:
            if abs(self.left_paddle_location - self.ball_y) <= self.paddle_size:
                self.ball_direction = self.ball_direction * -1
            else:
                return Players.Right

    def start(self, graphics):
        """Run the game"""
        winner = None
        while winner is None:
            self.move(Players.Left, self.left_ai.get_move(
                self.state(Players.Left)))
            self.move(Players.Right, self.right_ai.get_move(
                self.state(Players.Right)))
            graphics.update(self)

            winner = self.update()

        return (winner, self.length)
