import sys, pygame, random
pygame.init()
from collections import deque
from Card import Card

# notes
#  - card size 96w x 144h

# roadmap
#  - deck/discard info
#  - audio
#  - animation
#  - in game rules documentation
#  - other game types



# data declerations

    # scaling
scalingFactor = 1.5
screenSize = screenW, screenH = int(914 * scalingFactor) , int(512 * scalingFactor)
cardSize = cardW, cardH = int(96 * scalingFactor), int(144 * scalingFactor)
spacer = int(20 * scalingFactor)



black = 0, 0, 0
white = 255, 255, 255
poolFeltGreen = 39, 119, 20
poolFeltComplement = 119, 20, 40
poolFeltExtra = 31, 43, 71
moving = False
suits = ('spades', 'clubs', 'diamonds', 'hearts')
font = pygame.font.Font('freesansbold.ttf', 32)


# game data setup

    # castle deck setup
castle = deque([])

for i in range(3):
    subDeck = []

    for x in suits:
       subDeck.append(Card(x, i + 11, cardSize))

    random.shuffle(subDeck)
    castle.extend(subDeck)

for i in castle:
    if i.rank == 11:
        i.power = 10
        i.health = 20
    elif i.rank == 12:
        i.power = 15
        i.health = 30
    elif i.rank == 13:
        i.power = 20
        i.health = 40

    # tavern deck setup
tavern = deque([])

for i in range(10):
    for x in suits:
        tavern.append(Card(x, i + 1, cardSize))

random.shuffle(tavern)

    # discard setup
discard = []

    # hand setup
hand = []

for i in range(8):
    hand.append(tavern.pop())

discard.append(tavern[0])

    # attack setup
attack = []

# pygame setup

screen = pygame.display.set_mode([screenW, screenH])
pygame.display.set_caption('Regicide')

cardBack = pygame.image.load("assets\Playing Cards\card-back2.png")
cardBack = pygame.transform.scale(cardBack, cardSize)
cardBackRect = cardBack.get_rect()

joker = pygame.image.load("assets\Playing Cards\card-back1.png")
joker = pygame.transform.scale(joker, [cardW / 2, cardH / 2])
jokerRect1 = joker.get_rect()
jokerRect2 = joker.get_rect()

# main loop

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cardMoved = False
            for i in attack:
                if i.rect.collidepoint(event.pos) and cardMoved == False:
                    hand.append(attack.pop(attack.index(i)))
                    cardMoved = True
            for i in hand:
                if i.rect.collidepoint(event.pos) and cardMoved == False:
                    attack.append(hand.pop(hand.index(i)))
                    cardMoved = True

    power = font.render(f'Power: {castle[0].power}', True, poolFeltExtra)
    powerRect = power.get_rect()
    health = font.render(f'Health: {castle[0].health}', True, poolFeltComplement)
    healthRect = health.get_rect()

    screen.fill(poolFeltGreen)

    if len(castle) > 1: screen.blit(cardBack, (screenW - cardW - spacer, spacer), cardBackRect)
    screen.blit(castle[0].img, (screenW - spacer - cardW - (cardW / 4), spacer), castle[0].rect)

    if len(tavern) > 0: screen.blit(cardBack, (spacer, spacer), cardBackRect)
    if len(discard) > 0: screen.blit(discard[0].img, ((spacer * 2) + cardW, spacer), discard[0].rect)

    screen.blit(power, (screenW - (spacer * 2) - int(cardW * 1.25) - powerRect.w, spacer), powerRect)
    screen.blit(health, (screenW - (spacer * 3) - int(cardW * 1.25) - healthRect.w - powerRect.w, spacer),
                healthRect)

    screen.blit(joker, (screenW - 20 - (cardW / 2), int(spacer * 1.5) + cardH), jokerRect1)
    screen.blit(joker, (screenW - 20 - (cardW / 2), screenH - (int(spacer * 1.5) + int(cardH * 1.5))), jokerRect2)

    for i in hand:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * hand.index(i))
        i.rect.y = screenH - 20 - cardH
        screen.blit(i.img, i.rect)

    for i in attack:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * attack.index(i))
        i.rect.y = spacer * 2 + cardH
        screen.blit(i.img, i.rect)

    pygame.display.flip()