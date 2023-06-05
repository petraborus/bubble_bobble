"""
Author: Petra Borus
This program is for the re-make of the old classic 'Bubble Bobble'
There is a menu screen and one available level, in which the player (pink dragon) has to
try to shoot all the enemies (blue dragons) without losing their lives.
They can also gain points by shooting archery targets that appear and disappear randomly
"""

import pygame, sys
from button import Button
from settings import *
from level import *
from player import bullets

# initialise all pygame modules
pygame.init()
# basic screen where all the elements will be added
screen = pygame.display.set_mode((screen_width, screen_height))


# function for playing the level
def play():
    global screen
    clock = pygame.time.Clock()
    # uses level class to draw level with the level map set-up made in 'settings'
    level = Level(level_map, screen)

    while True:
        # quit game when user clicks 'x' on window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()

        screen.fill("black")
        level.run(bullets)
        # always check if player wins the game
        level.check_game_win()
        pygame.display.update()
        # clock set to 60 so  program will never run at more than 60 frames per second
        clock.tick(fps)
        if level.check_game_win():  # Check the game win condition
            return True


# function called when player shoots all enemies as an end screen
# note that there is no end screen for when the player loses all their lives
def game_over():
    global screen
    pygame.display.set_caption("Game Over")

    while True:
        screen.fill("black")
        menu_mouse_pos = pygame.mouse.get_pos()

        # create buttons with each attribute named that the Button class requires (see button file for credits)
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
            # though there is a play again button, both buttons are set to 'quit' atm as I didn't have time to make the play again work by resetting previous progress in the 'play' function
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
        # loads basic background image so I didn't need to add al the text separately
        screen.blit(pygame.transform.scale(pygame.image.load("graphics/game_bg.png"), (1400, 728)), (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        # create buttons with each attribute named that the Button class requires (see button file for credits)
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
                # calls play function
                if play_button.check_for_input(menu_mouse_pos):
                    game_won = play()  # Store the return value of play()
                    if game_won:
                        game_over()
                        break
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


# call main menu to start game
main_menu()







