import pygame
from settings import *
from support import import_folder
from arrow import Bullet

# need to give access to bullets, so class is imported and group is created
bullets = pygame.sprite.Group()


# player class to get animations and movement working
class Player(pygame.sprite.Sprite):
    # inherits abilities from pygame
    def __init__(self, pos):
        # call constructor for sprite before everything else
        super().__init__()

        # Graphics
        # dictionary locates graphics
        self.animations = {}
        # loads graphics
        self.import_character_assets()
        # frame index picks out first image in the respective list
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]

        # rectangle for decisions
        self.rect = self.image.get_rect(topleft=pos)

        # property to tell us the direction the player is going
        # vector is an x and y coordinate for movement
        # when (0, 0) it is stationary
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        # negative value as y-axis is 'inverted' and moving up is negative
        self.jump_speed = -16

        # Sounds
        # must create sound and then can be called later
        self.jump_sound = pygame.mixer.Sound("sounds/effects/player_jump.wav")
        self.jump_sound.set_volume(0.4)
        self.is_jumping = False  # Add a variable to track jump status
        self.jumping = False

        # Shooting
        self.bullets = bullets
        self.firing = False

        # Player orientation
        self.status = "idle"
        self.side = 1

    # imports animations based on what the status is
    def animate(self):
        # animation depends on the state of a player
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        # can't use a float as an index and can't go beyond number of images in list
        if self.frame_index >= len(animation):
            # goes back to first frame
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def import_character_assets(self):
        character_path = "graphics/player/"

        self.animations = {"idle":[], "jump":[], "walk":[], "walk_left":[], "idle_left":[], "jump_left":[]}

        # load image names into blank lists, loops through key names
        # key means 'idle' etc. --> uses a word instead of an index
        for animation in self.animations.keys():
            # attach rest to path
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # player movement
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            # changes direction to move to right
            self.direction.x = 1
            self.side = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.side = -1
        else:
            # stop movement if not pressing any keys
            self.direction.x = 0
        if keys[pygame.K_UP] and not self.jumping:
            if not self.jumping and not self.is_jumping:  # Check if the player is already jumping
                self.jumping = True
                self.jump()
        else:
            self.jumping = False  # Reset jump status when the up key is released
        if keys[pygame.K_SPACE] and not self.firing:
            # can fire when they aren't already doing so
            self.fire()
            self.firing = True
            # stops constant firing when holding down key
        elif not keys[pygame.K_SPACE] and self.firing:
            self.firing = False

    def fire(self):
        # creates bullet from the centre of the player and moves in the direction that the player is facing (by using 'side')
        bullet = Bullet((self.rect.centerx, self.rect.centery), self.side)
        self.bullets.add(bullet)

    def get_status(self):
        # checks for the status, also checking what the 'side' is to determine if the animations used should be facing the right or the left
        if self.direction.y < 0:
            if self.side == 1:
                self.status = "jump"
            else:
                self.status = "jump_left"
        else:
            # check to see if character isn't moving
            if self.direction.x == 0:
                if self.side == 1:
                    self.status = "idle"
                else:
                    self.status = "idle_left"
            else:
                if self.side == 1:
                    self.status = "walk"
                else:
                    self.status = "walk_left"

    def jump(self):
        # prevent double jump with status check
        if not self.is_jumping:  # Check if the player is already jumping
            self.is_jumping = True
            if self.side == 1:
                self.status = "jump"
            else:
                self.status = "jump_left"
            # goes against gravity - increases position
            self.direction.y = self.jump_speed
            # play sound when jumping occurs
            pygame.mixer.Sound.play(self.jump_sound)

    # prevents the player from going through the sides of the tiles
    def horizontal_movements_collision(self, tiles_general, tiles_edge):
        # change the players x coordinate depending on their direction and speed
        self.rect.x += self.direction.x * self.speed

        for tile in tiles_general.sprites():
            if tile.rect.colliderect(self.rect):
                # returns true if the player has touched the tile being checked, loop checks every tile
                if self.direction.x < 0:
                    # means they are moving to the left
                    self.rect.left = tile.rect.right
                elif self.direction.x > 0:
                    # pins player right-hand side to the left-hand side of the tile
                    self.rect.right = tile.rect.left

        for tile in tiles_edge.sprites():
            if tile.rect.colliderect(self.rect):
                # returns true if the player has touched the tile being checked, loop checks every tile
                if self.direction.x < 0:
                    # means they are moving to the left
                    self.rect.left = tile.rect.right
                elif self.direction.x > 0:
                    # pins player right-hand side to the left-hand side of the tile
                    self.rect.right = tile.rect.left

    def vertical_movements_collision(self, tiles_edge, tiles_general, tiles_portal):
        self.apply_gravity()

        for tile in tiles_general.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    # remove gravity when standing on a surface
                    self.direction.y = 0
                    # allow the player to jump again by setting status back to idle
                    if self.side == 1:
                        self.status = "idle"
                    else:
                        self.status = "idle_left"
            # no collision from teh bottom of the tile as I want the player to be able to jump onto the tile by going through it

        for tile in tiles_edge.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    # remove gravity when standing on a surface
                    self.direction.y = 0
                    if self.side == 1:
                        self.status = "idle"
                    else:
                        self.status = "idle_left"
                # if want to prevent going through the tiles when jumping up...
                if self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    if self.side == 1:
                        self.status = "idle"
                    else:
                        self.status = "idle_left"

        for tile in tiles_portal.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    # remove gravity when standing on a surface
                    self.direction.y = 0
                    if self.side == 1:
                        self.status = "idle"
                    else:
                        self.status = "idle_left"

        # set jumping back to false
        if self.direction.y >= 0:
            self.is_jumping = False
            self.jumping = False

    def apply_gravity(self):
        # constantly applies gravity
        self.direction.y += gravity
        # constant force that constantly gets bigger (as it falls, gets faster)
        self.rect.y += self.direction.y

    # function givees the illusion that if the player goes beyond a certain coordinate (where the purple tiles begin), they will appear on the other side of the screen, like going through a portal
    def portal(self):
        if self.rect.x > 1276:
            self.rect.x = 60
        if self.rect.x < 60:
            self.rect.x = 1276

    def update(self, tiles, enemies, tiles_general, tiles_edge, tiles_portal):
        # update direction, pass tiles info to see if collides
        self.get_input()
        self.get_status()
        self.vertical_movements_collision(tiles_edge, tiles_general, tiles_portal)
        self.horizontal_movements_collision(tiles_general, tiles_edge)
        self.portal()
        self.animate()
        self.bullets.update()

    def draw_bullets(self, surface):
        # draw all bullets to the screen
        self.bullets.draw(surface)




