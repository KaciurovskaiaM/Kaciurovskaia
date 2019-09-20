import sys
import pygame
import time
import random

pygame.init()

width = 500
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('YAHOOOO')
clock = pygame.time.Clock()

x = 130
y = 350
vx = 3
vy = 5
radius = 40
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

x1 = 200
y1 = 100
vx1 = 1
vy1 = 1
radius1 = 30
color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def move(x, y, vx, vy):
    x += vx
    y += vy
    return (x, y)

def vyhod(x, y, vx, vy):
    if y + radius >= height:
        if vy > 0:
            vy = -vy
        y = height - radius - 1

    if x + radius >= width:
        if vx > 0:
            vx = -vx
        x = width - radius - 1

    if y - radius <= 0:
        if vy < 0:
            vy = -vy
        y = 0 + radius + 1

    if x - radius <= 0:
        if vx < 0:
            vx = -vx
        x = 0 + radius + 1

    return (x, y, vx, vy)

def collision(x, y, x1, y1, vx, vy, vx1, vy1, radius, radius1):
    if ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5 <= radius + radius1:
        nx = x - x1
        ny = y - y1
        l = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        nx /= l
        ny /= l
        t = nx * vx + ny * vy
        t1 = nx * vx1 + ny * vy1
        k = (-ny) * vx + nx * vy
        k1 = (-ny) * vx1 + nx * vy1
        vx = t1 * nx + k * (-ny)
        vy = t1 * ny + k * nx
        vx1 = t * nx + k1 * (-ny)
        vy1 = t * ny + k1 * nx
    return (x, y, x1, y1, vx, vy, vx1, vy1, radius, radius1)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    (x, y) = move(x, y, vx, vy)
    (x1, y1) = move(x1, y1, vx1, vy1)

    (x, y, vx, vy) = vyhod(x, y, vx, vy)
    (x1, y1, vx1, vy1) = vyhod(x1, y1, vx1, vy1)

    (x, y, x1, y1, vx, vy, vx1, vy1, radius, radius1) = collision(x, y, x1, y1, vx, vy, vx1, vy1, radius, radius1)

    screen.fill((30, 90, 70))
    pygame.draw.circle(screen, color, (int(x), int(y)), radius)
    pygame.draw.circle(screen, color1, (int(x1), int(y1)), radius1)

    pygame.display.flip()
    time.sleep(0.01)
