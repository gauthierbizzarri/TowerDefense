import pygame
import os
from units.unit import Unit
import math
import random
class Conscrit(Unit) :

    imgs = []
    img = pygame.image.load(os.path.join("game_assets","soldier.png"))
    img = pygame.transform.scale(img, (50, 50))
    imgs.append(img)

    def __init__(self,ligne,colone,ally):
        super().__init__(ligne,colone,ally)
        self.range = 300
        self.inRange = False
        self.damage =random.randint(2,5)
        self.last = pygame.time.get_ticks()
        self.reload_time = 5000
        self.shooting = False
        self.reloading = False
    def attack(self,ennemies):
        enemy_closest = []
        print(ennemies)
        print("JE attaque")
        self.inRange = False
        distances = []
        for ennemy in ennemies :
            ennemy_x , ennemy_y = ennemy.x,ennemy.y
            dis = math.sqrt((self.x-ennemy_x)**2 + (self.y-ennemy_y)**2)
            distances.append(dis)
        if distances:
            ennemy_closest_distance =min(distances)
            index_closest = distances.index(ennemy_closest_distance)
            ennemy_closest = ennemies[index_closest]
            if ennemy_closest_distance <= self.range :
                self.inRange = True

        if self.inRange :
            now = pygame.time.get_ticks()
            if now - self.last >= self.reload_time:
                self.shooting = True
                self.last = now
                rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "musket.mp3"))
                rifle_sound.set_volume(0.7)
                pygame.mixer.Channel(1).play(rifle_sound)
                ennemy_closest.hit(self.damage)
        else :
            self.shooting = False

    def change_range(self,r):
        self.range = r
