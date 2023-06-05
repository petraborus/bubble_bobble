import pygame, random
from settings import *
from player import Player
from tile import *
from enemy import Enemy
from targets import Targets
from button import Button

# collision detection in level as it has access to both enemies and player groups

lives_text = ""
score_text = ""
you_lose_text = ""
win = False
font = ()
bigger_font = ()
targets_list = []
target_points = 0
enemy_points = 0
bullet_points = 0
score = 0
lives = 3


class Level:

    def __init__(self, level_data, surface):
        global lives_text, score_text, font, you_lose_text, bigger_font, final_score_text, score

        self.display_surface = surface
        self.tiles_general = pygame.sprite.Group()
        self.tiles_portal = pygame.sprite.Group()
        self.tiles_edge = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        # single group bc there is only one thing in the player group
        self.player = pygame.sprite.GroupSingle()
        # self.lives = 3
        # every object should be kept in a group
        self.enemies = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.enemy_fires = pygame.sprite.Group()
        self.time_counter = 0
        self.target_counter = 0

        self.setup_level(level_data)
        font = pygame.font.Font("VideoGame.ttf", 18)
        bigger_font = pygame.font.Font("VideoGame.ttf", 32)
        lives_text = font.render("LIVES LEFT: " + str(lives), True, "white")
        score_text = font.render("SCORE: " + str(score), True, "white")
        you_lose_text = bigger_font.render("You lost all your lives: TRY AGAIN", True, "white")

        pygame.mixer.music.load("sounds/music/game_music.mp3")
        # -1 makes it an indefinite loop
        pygame.mixer.music.play(-1)

    def setup_level(self, layout):
        global lives
        # loop through all the info from level map by row
        # one time when level is created

        # timer = time.perf_counter()

        for row_index, row in enumerate(layout):
            # will give row data and count until switch index
            for cell_index, cell in enumerate(row):
                # before if statement bc it is the same for tiles and player
                x = cell_index * tile_size
                # multiply bc otherwise it will only increase by one pixel each time, all tiles are in one corner
                y = row_index * tile_size
                if cell == "x":
                    tile = TileGeneral((x,y), tile_size)
                    self.tiles_general.add(tile)
                    self.tiles.add(tile)
                    # adds tile to group
                elif cell == "y":
                    tile = TileEdge((x,y), tile_size)
                    self.tiles_edge.add(tile)
                    self.tiles.add(tile)
                elif cell == "z":
                    tile = TilePortal((x,y), tile_size)
                    self.tiles_portal.add(tile)
                    self.tiles.add(tile)
                # create player in level because it needs to read p from map
                elif cell == "p":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                    # lives = self.player.sprite.number_of_lives

        for i in range(10):
            # create an enemy at a random position on the screen (x starts at 300)
            enemy = Enemy((random.randint(700, screen_width), random.randint(0, screen_height)))
            # add to enemies group
            self.enemies.add(enemy)

    def enemy_fire(self):
        # choose a random enemy to fire
        enemy_list = list(self.enemies)
        if len(enemy_list) > 0:
            random_enemy = random.choice(enemy_list)
            random_enemy.fire()

    def call_fire(self):
        self.time_counter += 1
        if self.time_counter == 30:
            self.enemy_fire()
            self.time_counter = 0

    def target_appears(self):
        # create a list of every non-special tile that the target could appear on
        tiles_list = list(self.tiles_general)
        # choose a random tile out of the list for 'random' element in target's appearance
        random_tile = random.choice(tiles_list)
        # use class to crate target and add to group
        target = Targets((random_tile.rect.x, random_tile.rect.y))
        self.targets.add(target)

    def call_target(self):
        global targets_list
        targets_list = list(self.targets)
        self.target_counter += 1
        if self.target_counter == 150:
            self.target_appears()
            self.target_counter = 0
            if len(targets_list) > 1:
                targets_list[0].kill()
                targets_list[0].remove()

    def off_screen(self):
        global lives
        if self.player.sprite.rect.y > 728:
            if lives > 1:
                lives -= 1
                self.player.sprite.rect.x = 468
                self.player.sprite.rect.y = 286
            else:
                lives = 0

    def check_game_win(self):
        if len(self.enemies) == 0:
            return True  # Return True if game is won
        return False  # Return False otherwise

    # now needs to actually draw the tiles
    # every time when it loops through the game
    def run(self, bullets):
        global lives_text, font, score_text, target_points, enemy_points, bullet_points, score, lives, enemies_shot

        self.tiles.draw(self.display_surface)

        # to update player location before it's drawn
        # sends enemies group so it has access to it
        self.player.update(self.tiles, self.enemies, self.tiles_general, self.tiles_edge, self.tiles_portal)
        self.player.draw(self.display_surface)
        self.player.sprite.draw_bullets(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.enemies.update(self.display_surface)
        self.targets.draw(self.display_surface)
        self.targets.update(self.display_surface)

        lives_text = font.render("LIVES LEFT: " + str(lives), True, "white")
        score_text = font.render("SCORE: " + str(score), True, "white")

        self.display_surface.blit(score_text, (1100, 15))
        self.display_surface.blit(lives_text, (8, 15))
        self.call_fire()
        self.call_target()
        self.off_screen()
        # Detect collisions between player and enemy

        # sprite collide can detect if a sprite collides with something in a group
        # gives a list of everything the player collides with
        collided_with = pygame.sprite.spritecollide(self.player.sprite, self.enemies, False)
        if len(collided_with) > 0:
            lives = 0

        player_is_shot = pygame.sprite.spritecollide(self.player.sprite, self.enemy_fires, False)
        if len(player_is_shot) > 0:
            lives -= 1
            # player_is_shot.pop()

        shooting_collision = pygame.sprite.groupcollide(self.player.sprite.bullets, self.enemies, True, True)
        score += 25*len(shooting_collision)

        target_shot = pygame.sprite.groupcollide(bullets, self.targets, True, True)
        score += 5*len(target_shot)

        enemy_fire_collision = pygame.sprite.spritecollide(self.player.sprite, self.enemy_fires, True, True)
        score += 2*len(enemy_fire_collision)

        '''
        # can get info like location of where the enemy was collided with
        for enemy in collided_with:
            print(enemy.rect.x, enemy.rect.y)
        # could create a 'setLife' attribute to player and deduct points upon collision
        if len(collided_with) > 0:
            self.player.setLife(-5)
        '''

