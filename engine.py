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
        # return f"ball\n\tpos = {self.pos}\n\tvel = {self.v}\n\tacc = {self.a}"
        return f"v0={self.v0}"

    def varied_copy(self, angle_variation, speed_variation):
        return Ball(self.pos0,
                    self.launch_speed + random.uniform(-speed_variation, speed_variation),
                    self.launch_angle + random.uniform(-angle_variation, angle_variation),
                    self.r, self.m, self.color)

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
        self.pos -= self.v * dt
        self.v -= (2 * self.v.dot(wall_norm) * randomized_wall_norm)
        self.v *= 1 - 0.2 * abs(norm(self.v).dot(randomized_wall_norm))

    def check_walls(self):
        if self.pos.y < field.wall_top.y:  # middle wall
            if self.pos.x > field.wall.x > (self.pos + self.v * dt).x:
                self.collide_with_wall(Vec(1, 0), field.WALL_RANDOMNESS())
            elif self.pos.x < field.wall.x < (self.pos + self.v * dt).x:
                self.collide_with_wall(Vec(-1, 0), field.WALL_RANDOMNESS())

        if field.horizontal_wall.p1.x < self.pos.x < field.horizontal_wall.p2.x:
            if self.pos.y > field.horizontal_wall.y > (self.pos + self.v * dt).y:
                self.collide_with_wall(Vec(0, 1), field.WALL_RANDOMNESS())
            elif self.pos.y < field.horizontal_wall.y < (self.pos + self.v * dt).y:
                self.collide_with_wall(Vec(0, -1), field.WALL_RANDOMNESS())

        if mag(self.pos - field.CENTER) > field.RADIUS:  # outer circular wall
            wall_norm = -norm(self.pos - field.CENTER)
            self.collide_with_wall(wall_norm, field.WALL_RANDOMNESS())

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
