import sys, pygame, random
pygame.init()
from collections import deque

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

class Card:
    def __init__(self, suit, rank, scale):
        self.suit = suit
        self.rank = rank
        self.img = pygame.transform.scale(pygame.image.load(f"assets\Playing Cards\card-{suit}-{rank}.png"), scale)
        self.rect = self.img.get_rect()
        self.power = rank
        self.health = 0

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
discard = deque([])

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

    screen.fill(poolFeltGreen)

    power = font.render(f'Power: {castle[0].power}', True, poolFeltExtra)
    powerRect = power.get_rect()
    screen.blit(power, (screenW - (spacer * 2) - int(cardW * 1.25) - powerRect.w, spacer), powerRect)

    health = font.render(f'Health: {castle[0].health}', True, poolFeltComplement)
    healthRect = health.get_rect()
    screen.blit(health, (screenW - (spacer * 3) - int(cardW * 1.25) - healthRect.w - powerRect.w, spacer),
                healthRect)

    atkPow = 0
    for i in attack: atkPow += i.power
    attackPow = font.render(f'Attack: {atkPow}', True, poolFeltComplement)
    attackPowRect = attackPow.get_rect()
    screen.blit(attackPow, (screenW - (spacer * 2) - (cardW / 2) - attackPowRect.w, int(spacer * 1.5) +
                            int(cardH * 1.25) - int(attackPowRect.h / 2)), attackPowRect)

    confirmAttack = font.render("Confirm Attack!", True, poolFeltComplement, black)
    confirmAttackRect = confirmAttack.get_rect()
    confirmAttackRect.x = screenW - (spacer * 2) - (cardW / 2) - confirmAttackRect.w
    confirmAttackRect.y = screenH - (int(spacer * 1.5) + int(cardH * 1.5)) + (cardW / 4)
    screen.blit(confirmAttack, confirmAttackRect)


    if len(castle) > 1: screen.blit(cardBack, (screenW - cardW - spacer, spacer), cardBackRect)
    screen.blit(castle[0].img, (screenW - spacer - cardW - (cardW / 4), spacer), castle[0].rect)

    if len(tavern) > 0: screen.blit(cardBack, (spacer, spacer), cardBackRect)
    if len(discard) > 0: screen.blit(discard[0].img, ((spacer * 2) + cardW, spacer), discard[0].rect)

    jokerRect1.x = screenW - spacer - (cardW / 2)
    jokerRect1.y = int(spacer * 1.5) + cardH
    screen.blit(joker, jokerRect1)

    jokerRect2.x = screenW - spacer - (cardW / 2)
    jokerRect2.y = screenH - (int(spacer * 1.5) + int(cardH * 1.5))
    screen.blit(joker, jokerRect2)

    for i in hand:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * hand.index(i))
        i.rect.y = screenH - 20 - cardH
        screen.blit(i.img, i.rect)

    for i in attack:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * attack.index(i))
        i.rect.y = spacer * 2 + cardH
        screen.blit(i.img, i.rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and confirmAttackRect.collidepoint(event.pos):
            spadesAbility = False
            diamondsAbility = False
            clubsAbility = False
            heartsAbility = False

            for i in attack:
                if i.suit == "spades" and castle[0].suit != "spades":
                    spadesAbility = True
                if i.suit == "diamonds" and castle[0].suit != "diamonds":
                    diamondsAbility = True
                if i.suit == "clubs" and castle[0].suit != "clubs":
                    clubsAbility = True
                if i.suit == "hearts" and castle[0].suit != "hearts":
                    heartsAbility = True

            if clubsAbility == True:
                atkPow = atkPow * 2
            if spadesAbility == True:
                print("TODO")
            if diamondsAbility == True:
                for i in range(atkPow):
                    if len(hand) < 8:
                        hand.append(tavern.popleft())
                    else:
                        break
            if heartsAbility == True:
                print("TODO")

            castle[0].health -= atkPow
            if castle[0].health == 0: tavern.appendleft(castle.popleft())
            elif castle[0].health < 0: discard.appendleft(castle.popleft())

            for i in range(len(attack)):
                discard.appendleft(attack.pop())

            if len(discard) > 0: print("d")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cardMoved = False
            for i in attack:
                if i.rect.collidepoint(event.pos) and cardMoved == False:
                    hand.append(attack.pop(attack.index(i)))
                    cardMoved = True
            for i in hand:
                if i.rect.collidepoint(event.pos) and len(attack) < 6 and cardMoved == False:
                    attack.append(hand.pop(hand.index(i)))
                    cardMoved = True