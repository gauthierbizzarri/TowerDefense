import sys , pygame
import os
from settings import *
from units import unit
class Game:
    def __init__(self):
        self.width = HEIGTH
        self.height = WIDTH
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.ennemies= []
        self.units = []
        self.money = int
        self.round = bool
        self.selected_units = unit
        self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))

        pygame.init()
        pygame.display.set_caption('Tower')
        self.clock = pygame.time.Clock()
    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run :
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
        pygame.quit()
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        pygame.display.update()

if __name__=='__main__':
    game = Game()
    game.run()