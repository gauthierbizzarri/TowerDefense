import pygame
from settings import *


def launch():
    """
    Start game
    """
    pygame.init()
    win =  pygame.display.set_mode((1920, 1080))
    from main_menu.main_menu import MainMenu

    mainMenu = MainMenu(win)
    mainMenu.run()


def run():
    pygame.init()
    win =  pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()


if __name__ == "__main__":
    launch()
launch()
