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

HOLE_POS = Vec(LEFT_WALL + 1, BOTTOM_WALL + 0.5)
BALL_POS0 = Vec(LEFT_WALL + 2, BOTTOM_WALL + 0.5)

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


wall_bottom = Vec(MIDDLE, 0)
wall_top = Vec(MIDDLE, 3)
wall = Wall(wall_bottom, wall_top)
