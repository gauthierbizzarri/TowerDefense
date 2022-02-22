import pygame
from settings import *


def launch():
    """
    Start game
    """
    pygame.init()
    win = pygame.display.set_mode((HEIGTH, WIDTH))
    from main_menu.main_menu import MainMenu

    mainMenu = MainMenu(win)
    mainMenu.run()


def run():
    pygame.init()
    win = pygame.display.set_mode((HEIGTH, WIDTH))
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()


if __name__ == "__main__":
    launch()
launch()
