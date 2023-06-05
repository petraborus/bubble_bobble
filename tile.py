import pygame


# inheritance to bring in class with functions
class TileGeneral(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#9d9b9bff")
        self.rect = self.image.get_rect(topleft=pos)


class TilePortal(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#531253ff")
        self.rect = self.image.get_rect(topleft=pos)


class TileEdge(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#9d9b9bff")
        self.rect = self.image.get_rect(topleft=pos)
