class Family:
    def __init__(self):
        self.family_score = 0
        self.balls = []
        self.generations_passed = 0

    def add(self, ball):
        self.balls.append(ball)

    def sort(self):
        self.balls = sorted(self.balls, key=lambda x: x.fitness)

    def calculate_family_score(self):
        score = sum([ball.fitness for ball in self.balls])/len(self.balls)
        return score
