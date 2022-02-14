import pygame
from settings import *
if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((HEIGTH, WIDTH))
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu(win)
    mainMenu.run()