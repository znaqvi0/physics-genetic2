import random

from vectors import *

WIDTH = 3
HEIGHT = 6
hole_radius = 0.05

LEFT_WALL = 0
RIGHT_WALL = WIDTH
BOTTOM_WALL = 0
TOP_WALL = HEIGHT
MIDDLE = 1.5

HOLE_POS = Vec(LEFT_WALL + 1.5, BOTTOM_WALL + 3)
BALL_POS0 = Vec(MIDDLE, BOTTOM_WALL + 0.2)

LEFT_WALL_NORM = Vec(1, 0)
RIGHT_WALL_NORM = Vec(-1, 0)
TOP_WALL_NORM = Vec(0, -1)
BOTTOM_WALL_NORM = Vec(0, 1)

WALL_RANDOMNESS = lambda: random.gauss(0, 0.1)


class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x = self.p1.x
        self.y = self.p1.y


bunker_left = Wall(Vec(LEFT_WALL + 1, BOTTOM_WALL + 2), Vec(LEFT_WALL + 1, BOTTOM_WALL + 4))
bunker_right = Wall(Vec(RIGHT_WALL - 1, BOTTOM_WALL + 2), Vec(RIGHT_WALL - 1, BOTTOM_WALL + 4))
bunker_bottom = Wall(Vec(LEFT_WALL + 1, BOTTOM_WALL + 2), Vec(RIGHT_WALL - 1, BOTTOM_WALL + 2))
