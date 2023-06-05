from os import walk
import pygame


def import_folder(path):

    surface_list = []
    # walks through folder, gives three pieces of information, the third will be the file name
    for _, __, img_files in walk(path):
        for file in img_files:
            if file != ".DS_Store":
                full_path = path + "/" + file
                # as looping through files, each is turned into a pygame images and placed into the list
                image = pygame.image.load(full_path)
                image = pygame.transform.scale(image, (74, 81))
                # each image added to list
                surface_list.append(image)
                # pygame.transform.flip(image, True, False)
    return surface_list
