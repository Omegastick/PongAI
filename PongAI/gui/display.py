import sys
import pygame
import time
import plotly.plotly as py
from plotly.graph_objs import *
from pygame.locals import *


class Display():
    """PyGame display for Pong"""
    def __init__(self):
        pygame.init()

        self.scale = 5

        self.size = self.width, self.height = 100 * self.scale, 100 * self.scale
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.screen = pygame.display.set_mode(self.size)

        pygame.font.init()
        self.font = pygame.font.SysFont('Courier New', 20)

        self.screen.fill(self.black)

        self.fast = True

        self.average_fitnesses = []
        self.highest_fitnesses = []

    def update(self, game):
        """Redraw the display"""
        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, self.white, ((game.ball_x - 2.5) * self.scale,
                                                   (game.ball_y - 2.5) *
                                                   self.scale,
                                                   5 * self.scale,
                                                   5 * self.scale))
        pygame.draw.rect(self.screen, self.white, (0,
                                                   (game.left_paddle_location -
                                                    game.paddle_size / 2) * self.scale,
                                                   5 * self.scale,
                                                   game.paddle_size * self.scale))
        pygame.draw.rect(self.screen, self.white, (self.width - (5 * self.scale),
                                                   (game.right_paddle_location -
                                                    game.paddle_size / 2) * self.scale,
                                                   5 * self.scale,
                                                   game.paddle_size * self.scale))
        textsurface = self.font.render(str(game.generation), False, self.white)
        self.screen.blit(textsurface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                trace0 = Scatter(x=list(range(len(self.average_fitnesses))), y=self.average_fitnesses)
                trace1 = Scatter(x=list(range(len(self.highest_fitnesses))), y=self.highest_fitnesses)
                data = Data([trace0, trace1])
                py.plot(data, filename = 'pong-ai')
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.fast = not self.fast

        if not self.fast:
            time.sleep(.005)

        pygame.display.update()
