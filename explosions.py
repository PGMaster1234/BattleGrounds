import pygame
import math
import random
import time

from levels import *

pygame.init()


# ---------------- Stuff
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1200, 650))
clock = pygame.time.Clock()
fps = 60
screen_width = screen.get_width()
screen_height = screen.get_height()
screen2 = pygame.Surface((screen_width, screen_height)).convert_alpha()
screen3 = pygame.Surface((screen_width, screen_height)).convert_alpha()
timer = 0
shake = [0, 0]

font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font50 = pygame.font.Font("freesansbold.ttf", 50)
font100 = pygame.font.Font("freesansbold.ttf", 100)

# ---------------- ColorSet
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
dark_blue = (32, 78, 128)
grey_dark_blue = (31, 46, 64)
greyer_dark_blue = (40, 50, 64)
blue = (68, 99, 144)
slightly_dark_blue = (58, 79, 114)
light_blue = (123, 186, 255)
extra_light_blue = (191, 222, 255)
red = (133, 78, 75)
dark_red = (132, 63, 76)
extra_dark_red = (131, 38, 67)


class ExplosiveColors:
    def __init__(self):
        pass
    white = (235, 237, 233)
    orange = (218, 134, 62)
    red = (117, 36, 5)
    cream = (232, 193, 112)
    purple = (36, 21, 39)
    blue = (21, 29, 40)


# ---------------- Objects
particlesL = []
sparksL = []
shockWavesL = []
explosiveSparksL = []
smokeL = []

# ---------------- Particle class


class Particle:
    def __init__(self, x, y, x_vel, y_vel, color, color2, size, decay, gravity, bounciness):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.color2 = color2
        self.size = size
        self.decay = decay
        self.gravity = gravity
        self.bounciness = bounciness

    def blit(self):
        pygame.draw.circle(screen2, self.color2, (self.x - self.size / 4, self.y + self.size / 4), self.size)
        pygame.draw.circle(screen2, self.color, (self.x, self.y), self.size)

    def move(self, blocks):
        self.x += (self.x_vel * dt)
        self.y += (self.y_vel * dt)
        self.y_vel += (self.gravity * dt)
        self.size -= (self.decay * dt)

        for b in blocks:
            if b.rect.collidepoint(self.x, self.y):
                if math.fabs(self.y - b.rect.top) < (self.y_vel + 10):
                    if self.y_vel > 0:
                        self.y = b.rect.top
                        self.y_vel *= -self.bounciness
                if math.fabs(self.x - b.rect.left) < (self.x_vel + 10):
                    self.x = b.rect.left
                    self.x_vel *= -self.bounciness
                if math.fabs(self.x - b.rect.right) < (self.x_vel + 10):
                    self.x = b.rect.right
                    self.x_vel *= -self.bounciness


# ---------------- Spark parent class
class Spark:
    def __init__(self, x, y, vel, color, color2, size, angle, decay, speed_decay, rotation, gravity, length):
        self.x = x
        self.y = y
        self.vel = vel
        self.color = color
        self.color2 = color2
        self.size = size
        self.angle = angle
        self.decay = decay
        self.gravity = gravity
        self.rotation = rotation
        self.speed_decay = speed_decay
        self.length = length

    def blit(self):
        points = [(self.x + (self.size * self.length/3 * math.cos(self.angle)) - self.size, self.y + (self.size * 2 * math.sin(self.angle)) + self.size),
                  (self.x + (self.size * math.cos(self.angle + math.pi / 2)) - self.size, self.y + (self.size * math.sin(self.angle + math.pi / 2)) + self.size),
                  (self.x + (self.size * 2 * self.length/3 * math.cos(self.angle + math.pi)) - self.size, self.y + (self.size * 3 * math.sin(self.angle + math.pi)) + self.size),
                  (self.x + (self.size * math.cos(self.angle - math.pi / 2)) - self.size, self.y + (self.size * math.sin(self.angle - math.pi / 2)) + self.size)]
        pygame.draw.polygon(screen2, self.color2, points)
        points = [(self.x + (self.size * self.length/3 * math.cos(self.angle)), self.y + (self.size * 2 * math.sin(self.angle))),
                  (self.x + (self.size * math.cos(self.angle + math.pi / 2)), self.y + (self.size * math.sin(self.angle + math.pi/2))),
                  (self.x + (self.size * 2 * self.length/3 * math.cos(self.angle + math.pi)), self.y + (self.size * 3 * math.sin(self.angle + math.pi))),
                  (self.x + (self.size * math.cos(self.angle - math.pi / 2)), self.y + (self.size * math.sin(self.angle - math.pi/2)))]
        pygame.draw.polygon(screen2, self.color, points)

    def move(self):
        self.x += self.vel * math.cos(self.angle) * dt
        self.y += self.gravity * dt
        self.y += self.vel * math.sin(self.angle) * dt
        self.size -= self.decay * dt
        self.rotation = 1 / (self.size * 20)
        if self.vel > 0:
            self.vel -= self.speed_decay * dt
        if 3 * math.pi / 2 > self.angle > math.pi / 2:
            self.angle -= self.rotation * dt
        if 5 * math.pi / 2 > self.angle > 3 * math.pi / 2:
            self.angle += self.rotation * dt
        if math.pi / 2 > self.angle > 0:
            self.angle += self.rotation * dt


# ---------------- Explosive Spark sub class
class ExplosiveSpark(Spark):
    def move(self):
        self.x += self.vel * math.cos(self.angle) * dt
        self.y += self.gravity * dt
        self.y += self.vel * math.sin(self.angle) * dt
        self.size -= self.decay * dt
        if self.vel > 0:
            self.vel -= self.speed_decay * dt
        self.length += self.decay * dt


# ---------------- Shockwave class
class Shockwave:
    def __init__(self, x, y, duration, size, max_size, width, color, color2, shadow):
        self.x = x
        self.y = y
        self.duration = duration
        self.size = size
        self.max_size = max_size
        self.width = width
        self.color = color
        self.color2 = color2
        self.shadow = shadow

    def expand(self):
        self.size += dt * (self.max_size-self.size)/(10 * self.duration)
        if self.size/self.max_size < 0.8:
            self.width -= 1 * dt
        else:
            self.width -= 2 * dt

    def blit(self):
        pygame.draw.circle(screen2, self.color2, (self.x - self.shadow, self.y + self.shadow), self.size, int(self.width))
        pygame.draw.circle(screen2, self.color, (self.x, self.y), self.size, int(self.width))


# ---------------- Parent block class
class Block:
    def __init__(self, x, y, w, h, depth, color, color2):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.color2 = color2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.shadow = pygame.Rect(self.x - depth, self.y + depth, self.w, self.h)

    def shadow(self):
        pygame.draw.rect(screen2, self.color2, self.shadow)

    def blit(self):
        pygame.draw.rect(screen2, self.color, self.rect)


# ---------------- Tiles
blocksL = []
tile_size = screen_width / 30
bx = 0
by = 0
for row in level1:
    bx = 0
    for tile in row:
        if tile == 1:
            blocksL.append(Block(tile_size * bx, tile_size * by, tile_size, tile_size, 5, dark_blue, grey_dark_blue))
        bx += 1
    by += 1


# ---------------- Smoke class
class Smoke:
    def __init__(self, x, y, x_vel, y_vel, color, size, decay):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.size = size
        self.decay = decay

    def move(self):
        self.x += self.x_vel * dt
        self.y -= self.y_vel * dt
        self.size -= self.decay * dt

    def blit(self):
        pygame.draw.circle(screen2, self.color, (self.x, self.y), self.size)


def explosion(spread_range):
    spread = spread_range
    for a in range(50):
        if random.randint(1, 5) == 1:
            particlesL.append(
                Particle(mx + random.uniform(-spread, spread), my + random.uniform(-spread, spread), random.uniform(-5, 5),
                         random.uniform(-5, 5), ExplosiveColors.white, ExplosiveColors.purple, random.uniform(30, 35),
                         random.uniform(0.2, 0.3), 0.1, 0.4))
        if random.randint(1, 5) == 1:
            particlesL.append(
                Particle(mx + random.uniform(-spread, spread), my + random.uniform(-spread, spread), random.uniform(-5, 5),
                         random.uniform(-5, 5), ExplosiveColors.orange, ExplosiveColors.purple, random.uniform(25, 30),
                         random.uniform(0.1, 0.2), 0.1, 0.4))
        if random.randint(1, 5) == 1:
            particlesL.append(
                Particle(mx + random.uniform(-spread, spread), my + random.uniform(-spread, spread), random.uniform(-5, 5),
                         random.uniform(-5, 5), ExplosiveColors.red, ExplosiveColors.purple, random.uniform(25, 30),
                         random.uniform(0.1, 0.2), 0.1, 0.4))
        if random.randint(1, 5) == 1:
            particlesL.append(
                Particle(mx + random.uniform(-spread, spread), my + random.uniform(-spread, spread), random.uniform(-5, 5),
                         random.uniform(-5, 5), ExplosiveColors.cream, ExplosiveColors.purple, random.uniform(25, 30),
                         random.uniform(0.1, 0.2), 0.1, 0.4))
        if random.randint(1, 3) == 1:
            smokeL.append(Smoke(mx + random.uniform(-spread * 5, spread * 5), my + random.uniform(-spread * 5, spread * 5), random.uniform(-spread / 8, spread / 8), random.uniform(spread / 3, spread / 2), ExplosiveColors.purple, random.uniform(30, 50), 0.2))
    for b in range(25):
        explosiveSparksL.append(
            ExplosiveSpark(mx + random.randint(-10, 10), my + random.randint(-10, 10), random.uniform(20, 28),
                           ExplosiveColors.white, ExplosiveColors.purple, random.uniform(15, 20),
                           random.uniform(0, math.pi * 2), 0.6, 0.8, 0, 0, 5))
    shockWavesL.append(Shockwave(mx, my, 1, 10, 100, 30, ExplosiveColors.white, ExplosiveColors.purple, 5))
    shockWavesL.append(Shockwave(mx, my, 1, 10, 250, 35, ExplosiveColors.white, ExplosiveColors.purple, 10))
    shockWavesL.append(Shockwave(mx, my, 1, 10, 400, 40, ExplosiveColors.white, ExplosiveColors.purple, 15))


# ---------------- Control board
last_time = time.time()
running = True
spawning_particles = False
spawning_sparks = False
spawning_shockWaves = False
spawning_explosions = True

while running:

    # ---------------- Reset stuff
    click = False
    mx, my = pygame.mouse.get_pos()
    screen.fill(greyer_dark_blue)
    screen2.fill(greyer_dark_blue)
    screen3.fill((0, 0, 0, 0))
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    timer -= 1 * dt
    shake = 0, 0

    # ---------------- Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # ---------------- Create Particles
    if spawning_particles:
        particlesL.append(Particle(mx, my, random.uniform(-2, 2), random.uniform(-2, 2), blue, slightly_dark_blue, random.randint(10, 15), random.uniform(0.2, 0.1), 0.1, 0.8))

    # ---------------- Particle stuff
    for p in particlesL:
        Particle.move(p, blocksL)
        Particle.blit(p)
        if random.randint(0, 20) == 1:
            smokeL.append(Smoke(p.x, p.y, p.x_vel * 0.1, 3, ExplosiveColors.purple, random.randint(8, 15), 0.05))
        if p.size < 0:
            smokeL.append(Smoke(p.x, p.y, p.x_vel * 0.1, 3, ExplosiveColors.purple, random.randint(8, 15), 0.05))
            particlesL.remove(p)

    # ---------------- Blocks stuff
    for block in blocksL:
        Block.shadow(block)

    for block in blocksL:
        Block.blit(block)

    # ---------------- Create sparks
    if spawning_sparks:
        for i in range(2):
            sparksL.append(Spark(mx, my, random.uniform(5, 6), dark_blue, slightly_dark_blue, random.uniform(3, 4), random.uniform(0, math.pi * 2), 0.05, 0.04, 0, 0, 15))

    # ---------------- Sparks stuff
    for s in sparksL:
        Spark.move(s)
        Spark.blit(s)
        if s.size < 0:
            sparksL.remove(s)

    # ---------------- Create shockwave
    if spawning_shockWaves:
        if click:
            shockWavesL.append(Shockwave(mx, my, 3, 10, 300, 50, light_blue, blue, 10))

    # ---------------- Shockwave stuff
    for shock in shockWavesL:
        Shockwave.expand(shock)
        Shockwave.blit(shock)
        if shock.width < 4:
            shockWavesL.remove(shock)

    # ---------------- Explosive Sparks stuff
    for spark in explosiveSparksL:
        ExplosiveSpark.move(spark)
        ExplosiveSpark.blit(spark)
        if spark.size < 1:
            explosiveSparksL.remove(spark)

    # ---------------- Smoke stuff
    for smoke in smokeL:
        Smoke.move(smoke)
        Smoke.blit(smoke)
        if smoke.size < 5:
            smokeL.remove(smoke)

    # ---------------- EXPLOSION
    if spawning_explosions:
        if click:
            timer = 30
            explosion(10)
    if timer > 0:
        shake = random.randint(-10, 10), random.randint(-10, 10)

    # ---------------- End frame
    pygame.mouse.set_visible(False)
    pygame.draw.circle(screen3, white, (mx, my), 5, 1)
    screen.blit(screen2, (shake[0], shake[1]))
    screen.blit(screen3, (0, 0))
    pygame.display.update()
    clock.tick(fps)
