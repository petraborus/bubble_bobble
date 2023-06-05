import pygame, sys
from button import Button
from settings import *
from level import *
from player import bullets

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))


def play():
    global screen, win
    clock = pygame.time.Clock()
    level = Level(level_map, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()

        screen.fill("black")
        level.run(bullets)
        level.check_game_win()
        pygame.display.update()
        clock.tick(fps)
        if level.check_game_win():  # Check the game win condition
            return True


def game_over():
    global screen
    pygame.display.set_caption("Game Over")

    while True:
        screen.fill("black")
        menu_mouse_pos = pygame.mouse.get_pos()

        play_again_button = Button(image=None, pos=(670, 508), text_input="PLAY AGAIN", font=pygame.font.Font("VideoGame.ttf", 40), base_colour="#d81e5b", hovering_colour="white")
        quit_button = Button(image=None, pos=(670, 600), text_input="QUIT", font=pygame.font.Font("VideoGame.ttf", 40), base_colour="#d81e5b", hovering_colour="white")

        for button in [play_again_button, quit_button]:
            button.change_colour(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # closes pygame and sys when user click on 'x' on screen
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks if mouse button has been clicked
                # checks for each button if it has been clicked and runs the required funtion
                if play_again_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


def main_menu():
    global screen
    pygame.display.set_caption("Menu")

    while True:
        screen.blit(pygame.transform.scale(pygame.image.load("graphics/game_bg.png"), (1400, 728)), (0, 0))
        # screen.fill("pink")

        menu_mouse_pos = pygame.mouse.get_pos()

        play_button = Button(image=None, pos=(670, 508), text_input="PLAY", font=pygame.font.Font("VideoGame.ttf", 40), base_colour="#d81e5b", hovering_colour="white")
        quit_button = Button(image=None, pos=(670, 600), text_input="QUIT", font=pygame.font.Font("VideoGame.ttf", 40), base_colour="#d81e5b", hovering_colour="white")

        for button in [play_button, quit_button]:
            button.change_colour(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # closes pygame and sys when user click on 'x' on screen
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks if mouse button has been clicked
                # checks for each button if it has been clicked and runs the required funtion
                if play_button.check_for_input(menu_mouse_pos):
                    game_won = play()  # Store the return value of play()
                    if game_won:
                        game_over()
                        break
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main_menu()







