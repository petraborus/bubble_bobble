import pygame
from settings import screen_width


# fire class assigns teh fires enemies shoot out a basic rectangle image, a 'rect', a speed, and directio
class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((30, 10))
        self.image.fill("#b8bae9")
        # intended graphic causes a lag in the game, so block was used instead
        # self.image = pygame.transform.scale(pygame.image.load("graphics/enemies/enemy_fire.png"), (52, 75))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 10
        self.direction = pygame.math.Vector2(direction * self.speed, 0)

    # to have the fires move horizontally after they are created instead of staying idle
    def update(self):
        self.rect.x += self.direction.x
        # get rid of bullets when off-screen so program doesn't have to calculate for it --> could cause performance issues later on
        if self.rect.x > screen_width or self.rect.x < 0:
            self.kill()
