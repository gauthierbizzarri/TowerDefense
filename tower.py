import sys , pygame
import os
import numpy as np
import random
from settings import *
from units import unit
from units.conscrit import Conscrit

pygame.font.init()
pygame.init()

pygame.mixer.music.load(os.path.join("game_assets", "music.mp3"))
class Game:
    def __init__(self):
        self.width = HEIGTH
        self.height = WIDTH
        self.l = 11
        self.c = 15
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.ennemies = []
        self.units = []
        self.moving_object = None
        self.money = int
        self.round = bool
        self.pause = True

        self.selected_units = unit
        self.bg = pygame.image.load(os.path.join("game_assets","bg.jpeg"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))
        self.clicks = []
        self.wave = 0
        pygame.display.set_caption('Tower')
        self.clock = pygame.time.Clock()
        self.MAT = self.matrice()

    def gen_ennemies_units(self):
        """
        generate the next enemy or enemies to show
        :return: enemy
        """
        wave_enemies = [Conscrit(0,0,False)]
        self.ennemies = wave_enemies
    def gen_units(self):
        allies = [Conscrit(0,0,True)]
        self.units = allies
    def run(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join("game_assets", "music.mp3")))
        run = True
        clock = pygame.time.Clock()
        self.matrice()
        while run :
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_ligne_col(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    if event.button==1:
                        ally = True

                    else :
                        ally =False
                    self.Add_unit(ally,self.get_ligne_col(pygame.mouse.get_pos()[0],
                                                          pygame.mouse.get_pos()[1])[0],self.get_ligne_col(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])[1])
                    #self.clicks.append(pos)

            self.draw()
            unites = []
            for k in range(len(self.ennemies)+len(self.units)):
                if k< len(self.ennemies):
                    unites.append(self.ennemies[k])
                if k < len(self.units):
                    unites.append(self.units[k])
            for unit in unites :

                if unit.health <= 0:
                    if unit.ally :
                        self.units.remove(unit)
                    else :
                        self.ennemies.remove(unit)
                    break
                if unit.ally:
                    unit.attack(self.ennemies)
                else :
                    unit.attack(self.units)
                unit.move()


        pygame.quit()

    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.drawGrid()
        for p in self.clicks:
            pygame.draw.circle(self.screen,(255,0,0),(p[0],p[1]),5,0)
            print(self.clicks)

        for en in self.ennemies:
             en.draw(self.screen)
        for unit in self.units:
            unit.draw(self.screen)

        pygame.display.update()

    def Add_unit(self,ally,ligne,col):
        object = Conscrit(ligne,col,ally)
        if ally :
            self.units.append(object)
        else :
            self.ennemies.append(object)
    def matrice(self):
        Mat = np.empty((self.l,self.c))

    def get_ligne_col(self,x,y):
        ligne = y//BLOCKSIZE
        col = x // BLOCKSIZE
        return ligne,col


    def drawGrid(self):
        blockSize = BLOCKSIZE  # Set the size of the grid block
        for x in range(self.c):
            for y in range(self.l):
                rect = pygame.Rect(x * blockSize, y * blockSize,
                                   blockSize, blockSize)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
if __name__=='__main__':
    game = Game()
    game.run()