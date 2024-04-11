import random

from vectors import *

hole_radius = 0.05

CENTER = Vec(0, 0)
RADIUS = 3
HOLE_POS = CENTER + Vec(0.5, 0.5) + Vec(-0.2, 0.2)
BALL_POS0 = CENTER + Vec(-0.5, -2.5)

WALL_RANDOMNESS = lambda: random.gauss(0, 0.1)


class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x = self.p1.x
        self.y = self.p1.y


wall_bottom = CENTER + Vec(0, -RADIUS)
wall_top = CENTER + Vec(0, 1)
wall = Wall(wall_bottom, wall_top)

horizontal_wall = Wall(wall.p2, wall.p2 + Vec(1, 0))
