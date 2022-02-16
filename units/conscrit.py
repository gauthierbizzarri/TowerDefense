import pygame
import os
from units.unit import Unit
import math
import random
from settings import *
imgs = []
img = pygame.image.load(os.path.join("game_assets","infanterie/imgs/conscrit.png"))
img = pygame.transform.scale(img, (BLOCKSIZE, BLOCKSIZE))
imgs.append(img)
class Conscrit(Unit) :


    def __init__(self,ligne,colone,ally):
        super().__init__(ligne,colone,ally)
        self.level = 0
        self.range = 10 * BLOCKSIZE
        self.proba_tir_reussi = 15
        self.proba_prendre_balle = 10
        self.proba_prendre_cac = 80
        self.proba_reussire_cac = 25

        self.inRange = False
        self.name ="Conscrit"
        self.price =price_conscrit
        self.last = pygame.time.get_ticks()
        self.reload_time = 25000
        self.shooting = False
        self.reloading = False
        self.imgs= imgs
        self.max_health = 10
        self.moral = 5
        self.health = self.max_health
        self.ammo = 15
        self.cac = False
        self.cac_reload = 2500
        self.cac_dommages = 20
        self.cacing = False

    def attack(self, ennemies):
        self.inRange = False
        ennemy_closest_distance = False
        distances = []
        ennemy_closest = None
        for ennemy in ennemies:
            ennemy_x, ennemy_y = ennemy.x, ennemy.y
            dis = math.sqrt((self.x - ennemy_x) ** 2 + (self.y - ennemy_y) ** 2)
            distances.append(dis)
        if distances:
            ennemy_closest_distance = min(distances)
            index_closest = distances.index(ennemy_closest_distance)
            ennemy_closest = ennemies[index_closest]
            if ennemy_closest_distance <= self.range:
                self.inRange = True
        if self.ammo <= 0:
            self.cac = True

        if ennemy_closest:
            ##ATTACKING WITH BAYONET
            print(ennemy_closest_distance)
            if self.cac and ennemy_closest_distance <= BLOCKSIZE:
                self.cacing = True
                now = pygame.time.get_ticks()
                if now - self.last >= self.cac_reload:
                    self.last = now
                    knife_sound = pygame.mixer.Sound(os.path.join("game_assets", "infanterie/sounds/knife.mp3"))
                    knife_sound.set_volume(0.3)
                    pygame.mixer.Channel(1).play(knife_sound)
                    ennemy_closest.hit(self.proba_reussire_cac,"c")

            if self.inRange and self.ammo > 0 and not self.cac:
                now = pygame.time.get_ticks()
                self.shooting = True
                if now - self.last >= self.reload_time:
                    self.last = now
                    rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infanterie/sounds/musket.mp3"))
                    rifle_sound.set_volume(0.3)
                    #pygame.mixer.Channel(1).play(rifle_sound)
                    ennemy_closest.hit(self.proba_tir_reussi,"t")
                    self.ammo -= 1



    def play_sound(self):
        pass

    def change_range(self,r):
        self.range = r
