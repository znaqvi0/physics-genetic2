import random

from vectors import *

width = 3
height = 6
hole_pos = Vec(0, 5)  # middle of field
hole_radius = 0.05

# ball_pos0 = lambda: Vec(0, 0.2)
ball_pos0 = Vec(0, 0.2)

left_wall = -width/2
right_wall = width/2
bottom_wall = 0
top_wall = height

left_wall_norm = Vec(1, 0)
right_wall_norm = Vec(-1, 0)
top_wall_norm = Vec(0, -1)
bottom_wall_norm = Vec(0, 1)

wall_randomness = lambda: random.gauss(0, 0.1)
