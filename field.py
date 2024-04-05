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

HOLE_POS = Vec(LEFT_WALL + 0.8, TOP_WALL - 0.8)
BALL_POS0 = Vec(MIDDLE, 0.2)

LEFT_WALL_NORM = Vec(1, 0)
RIGHT_WALL_NORM = Vec(-1, 0)
TOP_WALL_NORM = Vec(0, -1)
BOTTOM_WALL_NORM = Vec(0, 1)

WALL_RANDOMNESS = lambda: random.gauss(0, 0.1)


class Moat:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


hill_pos = Vec(1, 2)
valley_pos = Vec(2, TOP_WALL - 2)
hill_valley_radius = 1
