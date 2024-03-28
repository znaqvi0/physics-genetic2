from engine import Ball
from vectors import Vec


class Family:
    def __init__(self, population, sigma):
        self.family_score = 0
        self.balls = []
        self.generations_passed = 0
        self.population = population
        self.sigma = sigma
        self.best_ball = Ball(Vec(), 0, 0, 1, 1)

    def add(self, ball):
        self.balls.append(ball)

    def sort(self):
        self.balls = sorted(self.balls, key=lambda x: x.fitness)

    def calculate_family_score(self):
        score = sum([ball.fitness for ball in self.balls])/len(self.balls)
        return score

    def update(self):
        for ball in self.balls:
            ball.update()

    def all_done(self):
        for ball in self.balls:
            if not ball.done:
                return False
        return True

    def next_gen(self):
        self.balls = sorted(self.balls, key=lambda x: x.fitness, reverse=True)
        self.generations_passed += 1

        avg_distance = sum(ball.distance_from_hole() for ball in self.balls) / len(self.balls)
        # print(avg_distance)
        self.family_score = -avg_distance

        self.balls = self.balls[0:self.population // 3]  # // 50
        # global best_ball
        self.best_ball = self.balls[0]
        new_balls = []
        for ball in self.balls:
            for j in range(self.population // len(self.balls)):
                new_balls.append(ball.varied_copy_gaussian(self.sigma))

        self.sigma *= 0.9
        return new_balls

