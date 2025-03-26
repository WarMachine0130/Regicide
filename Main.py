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
phase = 'attack'
endTurn = False

class Card:
    def __init__(self, suit, rank, scale):
        self.suit = suit
        self.rank = rank
        self.img = pygame.transform.scale(pygame.image.load(f"assets\Playing Cards\card-{suit}-{rank}.png"), scale)
        self.rect = self.img.get_rect()
        self.power = rank
        self.health = 0
        self.penalty = 0

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
    hand.append(tavern.popleft())

discard.append(tavern[0])

    # attack setup
attack = []

# pygame setup

screen = pygame.display.set_mode([screenW, screenH])
pygame.display.set_caption('Regicide')

cardBack = pygame.image.load("assets\Playing Cards\card-back2.png")
cardBack = pygame.transform.scale(cardBack, cardSize)
tavernBackRect = cardBack.get_rect()
castleBackRect = cardBack.get_rect()

joker = pygame.image.load("assets\Playing Cards\card-joker-temp.png")
joker = pygame.transform.scale(joker, [cardW / 2, cardH / 2])
jokerRect1 = joker.get_rect()
jokerRect2 = joker.get_rect()

# main loop

while True:
    endTurn = False

    screen.fill(poolFeltGreen)

    power = font.render(f'Power: {castle[0].power - castle[0].penalty}', True, poolFeltExtra)
    powerRect = power.get_rect()
    powerRect.x = screenW - (spacer * 2) - int(cardW * 1.25) - powerRect.w
    powerRect.y = spacer
    screen.blit(power, powerRect)

    health = font.render(f'Health: {castle[0].health}', True, poolFeltComplement)
    healthRect = health.get_rect()
    healthRect.x = screenW - (spacer * 3) - int(cardW * 1.25) - healthRect.w - powerRect.w
    healthRect.y = spacer
    screen.blit(health, healthRect)

    atkPow = 0
    for i in attack: atkPow += i.power
    attackPow = font.render(f'Attack: {atkPow}', True, poolFeltComplement)
    attackPowRect = attackPow.get_rect()
    attackPowRect.x = screenW - (spacer * 2) - (cardW / 2) - attackPowRect.w
    attackPowRect.y = int(spacer * 1.5) + int(cardH * 1.25) - int(attackPowRect.h / 2)
    screen.blit(attackPow, attackPowRect)

    confirmAttack = font.render("Confirm Attack!", True, poolFeltComplement, black)
    confirmAttackRect = confirmAttack.get_rect()
    confirmAttackRect.x = screenW - (spacer * 2) - (cardW / 2) - confirmAttackRect.w
    confirmAttackRect.y = screenH - (int(spacer * 1.5) + int(cardH * 1.5)) + (cardW / 4)

    confirmDamage = font.render("Confirm Damage!", True, white, black)
    confirmDamageRect = confirmDamage.get_rect()
    confirmDamageRect.x = screenW - (spacer * 2) - (cardW / 2) - confirmDamageRect.w
    confirmDamageRect.y = screenH - (int(spacer * 1.5) + int(cardH * 1.5)) + (cardW / 4)

    if phase == 'attack':
        screen.blit(confirmAttack, confirmAttackRect)
        #screen.blit(confirmDamage, (10000, 10000), confirmDamageRect)

    elif phase == 'damage':
        screen.blit(confirmDamage, confirmDamageRect)
        #screen.blit(confirmAttack, (10000, 10000), confirmAttackRect)



    if len(castle) > 1:
        tavernBackRect.x = screenW - cardW - spacer
        tavernBackRect.y = spacer
        screen.blit(cardBack, tavernBackRect)

        castle[0].rect.x = screenW - spacer - cardW - (cardW / 4)
        castle[0].rect.y = spacer
        screen.blit(castle[0].img, castle[0].rect)

    if len(tavern) > 0:
        castleBackRect.x = spacer
        castleBackRect.y = spacer
        screen.blit(cardBack, castleBackRect)
    if len(discard) > 0:
        for i in discard:
            i.rect.x = (spacer * 2) + cardW
            i.rect.y = spacer
        screen.blit(discard[0].img, discard[0].rect)

    jokerRect1.x = screenW - spacer - (cardW / 2)
    jokerRect1.y = int(spacer * 1.5) + cardH
    screen.blit(joker, jokerRect1)

    jokerRect2.x = screenW - spacer - (cardW / 2)
    jokerRect2.y = screenH - (int(spacer * 1.5) + int(cardH * 1.5))
    screen.blit(joker, jokerRect2)

    for i in hand:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * hand.index(i))
        i.rect.y = screenH - spacer - cardH
        screen.blit(i.img, i.rect)

    for i in attack:
        i.rect.x = spacer + ((cardW + (spacer / 2)) * attack.index(i))
        i.rect.y = spacer * 2 + cardH
        screen.blit(i.img, i.rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and confirmAttackRect.collidepoint(event.pos) and phase == 'attack'
              and len(attack) > 0):
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
                castle[0].penalty = castle[0].penalty + atkPow
                if castle[0].penalty > castle[0].power: castle[0].penalty = castle[0].power
            if diamondsAbility == True:
                for i in range(atkPow):
                    if len(hand) < 8:
                        hand.append(tavern.popleft())
                    else:
                        break
            if heartsAbility == True:
                healedCards = []
                for i in range(atkPow):
                    try:
                        choice = random.choice(discard)
                        discard.remove(choice)
                        tavern.append(choice)
                    except :
                        break

            for i in range(len(attack)):
                discard.appendleft(attack.pop())

            castle[0].health -= atkPow
            if castle[0].health == 0: tavern.appendleft(castle.popleft())
            elif castle[0].health < 0: discard.appendleft(castle.popleft())
            elif castle[0].power - castle[0].penalty > 0:
                phase = 'damage'

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and confirmDamageRect.collidepoint(event.pos):
            if atkPow >= castle[0].power - castle[0].penalty:
                for i in range(len(attack)):
                    discard.appendleft(attack.pop())
                phase = 'attack'
                endTurn = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and phase == 'damage':
            cardMoved = False
            for i in hand:
                if i.rect.collidepoint(event.pos) and cardMoved == False and len(attack) < 6:
                    attack.append(hand.pop(hand.index(i)))
                    cardMoved = True

            for i in attack:
                if i.rect.collidepoint(event.pos) and cardMoved == False:
                    hand.append(attack.pop(attack.index(i)))
                    cardMoved = True

            cardMoved = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and phase == 'attack' and endTurn == False:
            cardMoved = False
            for i in hand:
                if i.rect.collidepoint(event.pos) and cardMoved == False and len(attack) < 6:
                    if len(attack) == 0: attack.append(hand.pop(hand.index(i)))
                    elif len(attack) == 1 and i.rank == 1: attack.append(hand.pop(hand.index(i)))
                    elif 1 < i.rank < 6 and i.rank == attack[0].rank:
                        count = 0
                        for j in attack: count += j.power
                        if count < 11: attack.append(hand.pop(hand.index(i)))

                    cardMoved = True

            for i in attack:
                if i.rect.collidepoint(event.pos) and cardMoved == False:
                    hand.append(attack.pop(attack.index(i)))
                    cardMoved = True

            cardMoved = True
            endTurn = True