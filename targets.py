import pygame
from settings import *


# targets class only has an image and a position, which will be used to create the targets in the level
class Targets(pygame.sprite.Sprite):

    def __init__(self, pos):
        self.image = pygame.transform.scale(pygame.image.load("graphics/target.png"), (78, 100))
        self.rect = self.image.get_rect(bottomleft=pos)



