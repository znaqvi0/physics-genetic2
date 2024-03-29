import sys  # most commonly used to turn the interpreter off (shut down your game)

import pygame as p

from engine import *
from families import Family

p.init()

WIDTH = 800
HEIGHT = 800
font = p.font.SysFont('Monocraft', 20)

screen_color = (0, 150, 150)
ground_color = (150, 150, 150)  # (50, 200, 100)
screen = p.display.set_mode((WIDTH, HEIGHT))
# screen.fill((150, 210, 255))
screen.fill(screen_color)
p.display.set_caption('window')

scale = 75  # 200
origin = x0, y0 = WIDTH / 2, HEIGHT - (field.TOP_WALL - field.BOTTOM_WALL) * scale / 2  # This is the new origin


def ball_xy(ball):
    return float(origin[0] + ball.pos.x * scale), float(origin[1] - ball.pos.y * scale)


def draw_ball(ball):
    p.draw.circle(screen, ball.color, ball_xy(ball), max(ball.r * scale, 1))


def make_display(text, top_left, text_color=(255, 255, 255), bg_color=None):
    display = font.render(text, True, text_color, bg_color)
    display_rect = display.get_rect()
    display_rect.topleft = top_left
    return display, display_rect


def draw_text(text, top_left, text_color=(255, 255, 255)):
    display, display_rect = make_display(text, (0, 0), text_color=text_color, bg_color=None)
    display_rect.topleft = top_left
    screen.blit(display, display_rect)


def draw_line(p1, p2):
    p.draw.line(screen, (0, 0, 0), (x0 + p1.x * scale, y0 - p1.y * scale),
                (x0 + p2.x * scale, y0 - p2.y * scale))


def draw_course():
    screen.fill(screen_color)
    p.draw.rect(screen, (0, 200, 50), (x0 + field.LEFT_WALL * scale,
                                       y0 - field.TOP_WALL * scale,
                                       (field.RIGHT_WALL - field.LEFT_WALL) * scale,
                                       (field.TOP_WALL - field.BOTTOM_WALL) * scale))
    draw_ball(Ball(field.HOLE_POS, 0, 0, 0.05, 1, color=(255, 255, 255)))

    draw_line(field.bunker_left.p1, field.bunker_left.p2)
    draw_line(field.bunker_right.p1, field.bunker_right.p2)
    draw_line(field.bunker_bottom.p1, field.bunker_bottom.p2)

    # p.draw.line(screen, (0, 0, 0),
    #             (x0 + field.wall.x * scale, y0 - field.wall.p1.y * scale),
    #             (x0 + field.wall.x * scale, y0 - field.wall.p2.y * scale))


# constants
pos0 = field.BALL_POS0
r = 0.021335
m = 0.045

initial_population = 10000
population = 1000
num_families = 20

sigma = 0.1  # sigma should be different for launch angle if using angle
# 0.5: 0.93 avg dist, 1: 1.01 avg
# test w/ 1000 varied copies of best ball after convergence, sigma=0.1

generation = 1

best_ball = Ball(Vec(), 0, 0, 1, 1)

test_family = Family(population, sigma)
# families = [test_family]
families = []


def random_ball():
    return Ball(pos0, random.uniform(0, 6), random.uniform(-180, 180), r, m,
                color=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))


def all_done(balls):
    for ball in balls:
        if not ball.done:
            return False
    return True


def all_families_done(families):
    for family in families:
        if not family.all_done():
            return False
    return True


for i in range(num_families):
    families.append(Family(population // num_families, sigma))
for family in families:
    for i in range(initial_population // num_families):
        family.add(random_ball())

draw_course()
running = False
sub_families_created = False
t = 0

while True:
    for event in p.event.get():
        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()
        elif event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:
                running = not running

    # screen.fill((150, 210, 255))  # comment/uncomment to enable/disable trail
    # draw_course()
    if running:
        for i in range(20):  # steps multiple times every frame, originally 2000//80
            for family in families:
                family.update()
            t += dt

        for family in families:
            for ball in family.balls:
                draw_ball(ball)

        if all_families_done(families):
            families = sorted(families, key=lambda fam: fam.family_score, reverse=True)
            print([fam.family_score for fam in families])

            if len(families) > 1 and sigma < 0.025:  # and sigma < 0.01:  # 0.001 | and generation >= 20:
                if generation % 5 == 0:  # kill off a family every _ generations
                    families.remove(families[-1])

                    for family in families:
                        family.population = population // len(families)

            best_ball = sorted(families, key=lambda fam: fam.best_ball.fitness, reverse=True)[0].best_ball
            sigma *= 0.9  # this will eventually family-dependent, just for display purposes
            for family in families:
                family.balls = family.next_gen()

                screen.fill(screen_color)
                draw_course()

            if best_ball is not None:
                generation += 1

                # draw_text("launch angle: %.5f degrees" % best_ball.launch_angle, (20, 20))
                # draw_text("launch speed: %.5f m/s" % best_ball.launch_speed, (20, 40))
                draw_text(best_ball.__repr__(), (20, 40))
                draw_text("sigma: %.10f" % families[0].sigma, (20, 60))
                draw_text("fitness: %.5f" % best_ball.fitness, (20, 80))
                draw_text("generation: %.0i" % generation, (20, 100))
                draw_text("best family score: %.5f" % families[0].family_score, (20, 120))  # check

    p.display.flip()
    p.time.Clock().tick(100)  # caps frame rate at 100
