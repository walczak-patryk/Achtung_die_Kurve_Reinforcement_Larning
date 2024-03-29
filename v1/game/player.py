from math import cos, radians, sin
import random

import pygame

from v1.game.config import BLACK, WINDOW_BORDER


class Player():
    def __init__(self, border:int = WINDOW_BORDER):
        self.active = True
        self.color = None
        self.score = 0
        self.radius = 2
        self.x = 0
        self.y = 0
        self.angle = 0
        self.border = border

    def gen(self, game):
        self.x = random.randrange(self.border, game.window_width - self.border)
        self.y = random.randrange(self.border, game.window_height - self.border)
        self.angle = random.randrange(0, 360)

    def move(self):
        self.x += int(self.radius * 2 * cos(radians(self.angle)))
        self.y += int(self.radius * 2 * sin(radians(self.angle)))

    def draw(self, game):
        pygame.gfxdraw.aacircle(game.display, self.x,
                                self.y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(
            game.display, self.x, self.y, self.radius, self.color)

    def collision(self, game):
        if (self.x > game.window_width-game.window_buffer or self.x < game.window_buffer or
            self.y > game.window_height-game.window_buffer or self.y < game.window_buffer or
            (game.frame != 0 and game.display.get_at((self.x, self.y)) != BLACK)):
            self.active = False
            return True
        else:
            return False

    def angle_reset(self):
        if self.angle < 0:
            self.angle += 360
        elif self.angle >= 360:
            self.angle -= 360