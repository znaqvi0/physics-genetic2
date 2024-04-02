from engine import Ball
from vectors import Vec
import numpy as np


class Family:
    def __init__(self, population, sigma):
        self.family_score = 0
        self.balls = []
        self.generations_passed = 0
        self.population = population
        self.sigma = sigma
        self.best_ball = Ball(Vec(), 0, 0, 1, 1)
        self.last_family = False

    def add(self, ball):
        self.balls.append(ball)

    def sort(self):
        self.balls = sorted(self.balls, key=lambda x: x.fitness)

    def calculate_family_score(self):
        score = sum([ball.fitness for ball in self.balls]) / len(self.balls)
        return score

    def update(self):
        for ball in self.balls:
            ball.update()

    def all_done(self):
        for ball in self.balls:
            if not ball.done:
                return False
        return True

    def tribalism(self, num_families):
        new_families = []
        lst = sorted(self.balls, key=lambda x: x.personality())
        sections = np.array_split(lst, num_families)
        for i in range(len(sections)):  # for every section
            new_families.append(Family(self.population // num_families, self.sigma))
            for ball in sections[i]:  # add every ball in the section to the corresponding family
                new_families[i].add(ball)
        return new_families

    def next_gen(self):
        self.balls = sorted(self.balls, key=lambda x: x.fitness, reverse=True)
        self.generations_passed += 1

        avg_distance = sum(ball.distance_from_hole() for ball in self.balls) / len(self.balls)
        self.family_score = -avg_distance

        success_balls = [ball for ball in self.balls if ball.distance_from_hole() == 0.0]
        # include all successful balls at minimum clamp b/w pop//5 and pop//2
        if not self.last_family:
            num_balls_to_reproduce = max(self.population // 5, min(len(success_balls), self.population//2))
        else:
            num_balls_to_reproduce = self.population // 5
        self.balls = self.balls[0:num_balls_to_reproduce]
        self.best_ball = self.balls[0]
        new_balls = []
        for ball in self.balls:
            for j in range(self.population // len(self.balls)):
                new_balls.append(ball.varied_copy_gaussian(self.sigma))

        self.sigma *= 0.9
        return new_balls


# if __name__ == "__main__":
#     fam = Family(500, 0.1)
#     for i in range(fam.population):
#         fam.add(deoxyribonucleic_acid.random_ball())
#     print(fam.tribalism(10)[0].balls)
