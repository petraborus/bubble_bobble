import pygame, random
from settings import *
from fire import Fire


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/enemies/blue_dragon.png"), (74, 81))
        self.rect = self.image.get_rect(topleft=pos)
        self.fires = pygame.sprite.Group()

    def update(self, display_surface):
        # everytime that the game updates, enemy moves its x and y coordinates randomly
        self.rect.x += random.randint(-5, 5)
        self.rect.y += random.randint(-5, 5)
        # keep enemies to desired screen limit
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600

        self.fires.update()
        self.fires.draw(display_surface)

    def fire(self):
        fire = Fire((self.rect.x, self.rect.y), -1)
        self.fires.add(fire)

