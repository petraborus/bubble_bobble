import pygame


# inheritance to bring in class with functions
# each tile is a simple, coloured square that will be draw to the level screen

# general tiles: can go through bottom when jumping up
class TileGeneral(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#9d9b9bff")
        self.rect = self.image.get_rect(topleft=pos)


# portal tiles: different colour to signify that they are a 'portal'
class TilePortal(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#531253ff")
        self.rect = self.image.get_rect(topleft=pos)


# edge tiles: same as general, but can't go through the bottom (so that when tiles are stacked, player can't just shoot up to the top
class TileEdge(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("#9d9b9bff")
        self.rect = self.image.get_rect(topleft=pos)
