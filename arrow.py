import pygame
from settings import screen_width


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((30, 10))
        self.image.fill("#d81e5b")
        self.rect = self.image.get_rect(topleft=pos)
        # do a check so that even if tge player isn't moving, bullet is still shot
        self.speed = 10
        self.direction = pygame.math.Vector2(direction * self.speed, 0)

    def update(self):
        self.rect.x += self.direction.x
        # get rid of bullets when off-screen so program doesn't have to calculate for it --> could cause performance issues later on
        if self.rect.x > screen_width or self.rect.x < 0:
            self.kill()

