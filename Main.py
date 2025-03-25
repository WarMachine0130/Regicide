import sys, pygame
pygame.init()

import random

from Card import Card
from Stack import Stack


size = width, height = 800, 600
speed = [2, 2]
black = 0, 0, 0
poolFeltGreen = 39, 119, 20

screen = pygame.display.set_mode((size), pygame.RESIZABLE)
pygame.display.set_caption('Test')

ball = pygame.image.load("assets\Playing Cards\card-spades-1.png")
ballrect = ball.get_rect()
#ballrect.center = width//2, height//2

moving = False
suits = ['spades', 'clubs', 'diamonds', 'hearts']

# game setup

# castle deck setup
castle = Stack()

for i in range(3):
    stack = Stack()

    for x in suits:
        stack.contents.append(Card(x, i + 11, f"assets\Playing Cards\card-{x}-{i + 11}.png"))

    random.shuffle(stack.contents)
    castle.contents.extend(stack.contents)


for i in castle.contents:
    print(f"{i.rank} of {i.suit}")

# tavern deck setup
tavern = Stack()

for i in range(10):
    for x in suits:
        tavern.contents.append(Card(x, i + 1, f"assets\Playing Cards\card-{x}-{i + 1}.png"))
random.shuffle(tavern.contents)

print("")

for i in tavern.contents:
    print(f"{i.rank} of {i.suit}")

while True:
    pygame.draw.rect(screen, "white", ballrect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ballrect.collidepoint(event.pos):
                moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
        elif event.type == pygame.MOUSEMOTION and moving:
            ballrect.move_ip(event.rel)

            #ballrect = ballrect.move(speed)
    #if ballrect.left < 0 or ballrect.right > width:
        #speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
        #speed[1] = -speed[1]

    screen.fill(poolFeltGreen)
    screen.blit(ball, ballrect)
    pygame.display.flip()