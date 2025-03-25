import sys, pygame
pygame.init()

import random

from Card import Card
from Stack import Stack

# notes
#  - card size 96w x 144h

# roadmap
#  - deck/discard info
#  - audio
#  - animation
#  - in game rules documentation
#  - other game types



# data declerations


size = width, height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255
poolFeltGreen = 39, 119, 20
moving = False
suits = ('spades', 'clubs', 'diamonds', 'hearts')


# game data setup

    # castle deck setup
castle = Stack()

for i in range(3):
    stack = Stack()

    for x in suits:
        stack.contents.append(Card(x, i + 11))

    random.shuffle(stack.contents)
    castle.contents.extend(stack.contents)


for i in castle.contents:
    print(f"{i.rank} of {i.suit}")

    # tavern deck setup
tavern = Stack()

for i in range(10):
    for x in suits:
        tavern.contents.append(Card(x, i + 1))
random.shuffle(tavern.contents)

    # discard setup
discard = Stack()

discard.contents.append(tavern.contents[0])

# pygame setup

screen = pygame.display.set_mode((size), pygame.RESIZABLE)
pygame.display.set_caption('Regicide')

cardBack = pygame.image.load("assets\Playing Cards\card-back2.png")
cardBackRect = cardBack.get_rect()

castleDeck = pygame.image.load(castle.contents[0].filePath)
castleDeckRect = castleDeck.get_rect()
castleDeckRect.x = width - 140
castleDeckRect.y = 20

discardTop = pygame.image.load(discard.contents[0].filePath)
discardTopRect = discardTop.get_rect()

# main loop

while True:
   # pygame.draw.rect(screen, "white", ballrect)



    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if castleDeckRect.collidepoint(event.pos): moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
            castleDeckRect.x = width - 140
            castleDeckRect.y = 20

        elif event.type == pygame.MOUSEMOTION and moving: castleDeckRect.move_ip(event.rel)

    screen.fill(poolFeltGreen)

    screen.blit(cardBack, (width - 116, 20), cardBackRect)
    screen.blit(castleDeck, castleDeckRect)
    if len(tavern.contents) > 0: screen.blit(cardBack, (20, 20), cardBackRect)
    if len(discard.contents) > 0: screen.blit(discardTop, (20, 184), discardTopRect)




    pygame.display.flip()
