import pygame
from settings import *


class Targets(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        # self.image = pygame.Surface((32, 80))
        # self.image.fill("pink")
        self.image = pygame.transform.scale(pygame.image.load("graphics/target.png"), (78, 100))
        self.rect = self.image.get_rect(bottomleft=pos)



