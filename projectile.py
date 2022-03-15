import pygame
import math
import os
from settings import *


class Projectile():
    def __init__(self, x, y):
        self.x = x+10
        self.y = y
        self.line,self.col = int(self.y // BLOCKSIZE), int(self.x // BLOCKSIZE)
        self.slug = "ball"
        self.hitten_cpt = 0
        self.cibles = []

    def draw(self, surface, pos):
        images=[pygame.image.load(os.path.join("game_assets/infantry/images/ball" + ".png")).convert_alpha(), \
              (BLOCKSIZE / 3, BLOCKSIZE / 3)]
        image = images[0]
        canon = pygame.transform.scale(image, (25, 25))
        surface.blit(canon, (self.x - pos+BLOCKSIZE, self.y+BLOCKSIZE+30))
