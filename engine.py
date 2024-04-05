import random

import field
from vectors import *

dt = 0.01  # 0.001


class Ball:
    def __init__(self, position, launch_speed, launch_angle, radius, mass, color=(0, 0, 0)):
        self.v = Vec(math.cos(math.radians(launch_angle)),
                     math.sin(math.radians(launch_angle)),
                     0) * launch_speed
        self.v0 = Vec(math.cos(math.radians(launch_angle)),
                      math.sin(math.radians(launch_angle)),
                      0) * launch_speed
        self.pos = position
        self.pos0 = position
        self.a = Vec()
        self.r = radius
        self.m = mass
        self.color = color
        self.done = False
        self.t = 0
        self.max_height = 0
        self.launch_angle = launch_angle
        self.launch_speed = launch_speed
        self.range = 0

        self.fitness = 0

    def __repr__(self):
        return f"v0={self.v0}"

    def varied_copy_gaussian(self, sigma):
        ball = Ball(self.pos0,
                    random.gauss(self.launch_speed, sigma),
                    random.gauss(self.launch_angle, sigma),
                    self.r, self.m, self.color)
        ball.v = Vec(random.gauss(self.v0.x, sigma), random.gauss(self.v0.y, sigma))
        ball.v0 = ball.v.copy()
        return ball

    def move(self):
        self.pos += self.v * dt
        self.a = self.force() / self.m
        self.v += self.a * dt

    def distance_from_hole(self):
        return mag(self.pos - field.HOLE_POS) if not self.in_hole() else 0

    def calculate_fitness(self):
        score = -self.distance_from_hole()
        return score

    def personality(self):
        return math.atan2(self.v0.x, self.v0.y) + mag(self.v0)

    def friction(self):
        return -0.015 * norm(self.v)

    def force(self):
        return self.friction()

    def in_hole(self):
        return mag(self.pos - field.HOLE_POS) <= (-1.0 / 32) * mag(self.v) + field.hole_radius

    def collide_with_wall(self, wall_norm, sigma):
        randomized_wall_norm = wall_norm.rotate(random.gauss(0, sigma), degrees=True)
        self.v -= (2 * self.v.dot(wall_norm) * randomized_wall_norm)
        self.v *= 1 - 0.2 * abs(norm(self.v).dot(randomized_wall_norm))

    def check_walls(self):
        if self.pos.x < field.LEFT_WALL:
            self.collide_with_wall(field.LEFT_WALL_NORM, field.WALL_RANDOMNESS())
        elif self.pos.x > field.RIGHT_WALL:
            self.collide_with_wall(field.RIGHT_WALL_NORM, field.WALL_RANDOMNESS())
        if self.pos.y < field.BOTTOM_WALL:
            self.collide_with_wall(field.BOTTOM_WALL_NORM, field.WALL_RANDOMNESS())
        elif self.pos.y > field.TOP_WALL:
            self.collide_with_wall(field.TOP_WALL_NORM, field.WALL_RANDOMNESS())

        if self.pos.y < field.wall_top.y:
            if self.pos.x > field.wall.x > (self.pos + self.v * dt).x:
                self.collide_with_wall(Vec(1, 0), field.WALL_RANDOMNESS())
            elif self.pos.x < field.wall.x < (self.pos + self.v * dt).x:
                self.collide_with_wall(Vec(-1, 0), field.WALL_RANDOMNESS())

    def update(self):
        if mag(self.v) > 0.005 and not self.in_hole():
            self.check_walls()
            self.move()
            self.t += dt
        else:
            if not self.done:
                self.fitness = self.calculate_fitness()
                string = ""
                string += str(self.fitness)
                # print(string)
            self.done = True
