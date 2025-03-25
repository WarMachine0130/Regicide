import pygame
class Card:
    def __init__(self, suit, rank, scale):
        self.suit = suit
        self.rank = rank
        self.img = pygame.transform.scale(pygame.image.load(f"assets\Playing Cards\card-{suit}-{rank}.png"), scale)
        self.rect = self.img.get_rect()
        self.power = rank
        self.health = 0

