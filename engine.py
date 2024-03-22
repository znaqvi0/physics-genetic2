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
        return f"ball\n\tpos = {self.pos}\n\tvel = {self.v}\n\tacc = {self.a}"

    def varied_copy(self, angle_variation, speed_variation):
        return Ball(self.pos0,
                    self.launch_speed + random.uniform(-speed_variation, speed_variation),
                    self.launch_angle + random.uniform(-angle_variation, angle_variation),
                    self.r, self.m, self.color)

    def varied_copy_gaussian(self, sigma):
        return Ball(self.pos0,
                    random.gauss(self.launch_speed, sigma),
                    random.gauss(self.launch_angle, sigma),
                    self.r, self.m, self.color)

    def move(self):
        self.pos += self.v * dt
        self.a = self.force() / self.m
        self.v += self.a * dt

    def distance_from_hole(self):
        return mag(self.pos - field.HOLE_POS) if not self.in_hole() else 0

    def calculate_fitness(self):
        # TODO based on distance from hole & whether there is a wall in ball-hole line of sight
        # score = -mag(self.pos - field.HOLE_POS) - 0.1 * self.launch_speed  # - (2 if self.in_any_moat() else 0)
        score = -self.distance_from_hole() - 0.1 * self.launch_speed
        return score

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

    def in_moat(self, moat):
        return moat.left < self.pos.x < moat.right and moat.bottom < self.pos.y < moat.top

    def in_any_moat(self):
        return self.in_moat(field.left_moat) or self.in_moat(field.right_moat)

    def check_walls(self):
        if self.pos.x < field.LEFT_WALL:
            self.collide_with_wall(field.LEFT_WALL_NORM, field.WALL_RANDOMNESS())
        elif self.pos.x > field.RIGHT_WALL:
            self.collide_with_wall(field.RIGHT_WALL_NORM, field.WALL_RANDOMNESS())
        if self.pos.y < field.BOTTOM_WALL:
            self.collide_with_wall(field.BOTTOM_WALL_NORM, field.WALL_RANDOMNESS())
        elif self.pos.y > field.TOP_WALL:
            self.collide_with_wall(field.TOP_WALL_NORM, field.WALL_RANDOMNESS())

        if self.in_any_moat():
            self.v = Vec()

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
                # string += f"launch angle: %.5f " % self.launch_angle
                # string += f", launch speed: {round(self.launch_speed, 5)}"
                # print(string)
            self.done = True
