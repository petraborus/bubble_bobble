import pygame, random
from settings import *
from fire import Fire


# This class sets the attributes of the 10 enemies that appear in the game
class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/enemies/blue_dragon.png"), (74, 81))
        self.rect = self.image.get_rect(topleft=pos)
        # collects all the bullets of the enemies in a group
        self.fires = pygame.sprite.Group()

    def update(self, display_surface):
        # everytime that the game updates, enemy moves its x and y coordinates randomly by a value between -5 and 5
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

    # function to create the bullets the enemies shoot out, giving it the position of an enemy and the direction as -1 meaning they always shoot to the left
    def fire(self):
        fire = Fire((self.rect.x, self.rect.y), -1)
        # add each fire to the group
        self.fires.add(fire)

