import pygame
import math
import random
import time
import json
pygame.init()

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
scroll = [0, 0]

font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font50 = pygame.font.Font("freesansbold.ttf", 50)
font100 = pygame.font.Font("freesansbold.ttf", 100)

# ---------------- Import blocks
blocks = []
blocksize = 50

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

# ---------------- Control board
last_time = time.time()
running = True

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

    # ---------------- Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # ---------------- Block picker
    pygame.draw.rect(screen2, grey_dark_blue, pygame.Rect(0, 0, 250, screen_height))
    counter = 0
    for block in blocks:
        x = 10
        y = 10
        counter += 1
        if counter > 10:
            x += blocksize
            counter = 0
        screen2.blit(block, (x, y + blocksize * counter))

    # ---------------- End frame
    
    pygame.mouse.set_visible(False)
    pygame.draw.circle(screen3, white, (mx, my), 5, 1)
    screen.blit(screen2, (shake[0], shake[1]))
    screen.blit(screen3, (0, 0))
    pygame.display.update()
    clock.tick(fps)
