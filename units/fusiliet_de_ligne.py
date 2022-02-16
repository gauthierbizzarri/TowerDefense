import pygame
import os
from units.unit import Unit
import math
import random
from settings import *
imgs = []
img = pygame.image.load(os.path.join("game_assets","infanterie/imgs/tirailleur.png"))
img = pygame.transform.scale(img, (BLOCKSIZE, BLOCKSIZE))
imgs.append(img)

class Infanterie_de_ligne(Unit) :
    def __init__(self, ligne, colone, ally):
        super().__init__(ligne, colone, ally)
        self.level = 1
        self.range = 10 * BLOCKSIZE
        self.proba_tir_reussi = 20
        self.proba_prendre_balle = 10
        self.proba_prendre_cac = 70
        self.proba_reussire_cac = 40
        self.last = pygame.time.get_ticks()
        self.reload_time = 23000
        self.shooting = False
        self.reloading = False
        self.imgs = imgs
        self.max_health = 15
        self.health = self.max_health
        self.ammo = 15
        self.name = "Infanterie_de_ligne"
        self.cac = False
        self.cac_reload = 2500
        self.cac_dommages = 20
        self.cacing = False
        self.price = price_infanterie_de_ligne

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
            if self.cac and ennemy_closest_distance <= BLOCKSIZE:
                now = pygame.time.get_ticks()
                self.cacing = True
                if now - self.last >= self.cac_reload:
                    self.last = now
                    knife_sound = pygame.mixer.Sound(os.path.join("game_assets", "infanterie/sounds/knife.mp3"))
                    knife_sound.set_volume(0.3)
                    pygame.mixer.Channel(1).play(knife_sound)
                    ennemy_closest.hit(self.proba_reussire_cac,"c")
                    return
            else :
                self.cacing = False
            if self.inRange and self.ammo > 0 and not self.cac:
                now = pygame.time.get_ticks()
                self.shooting = True
                if now - self.last >= self.reload_time:
                    self.last = now
                    rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infanterie/sounds/musket.mp3"))
                    rifle_sound.set_volume(0.3)
                    #ygame.mixer.Channel(1).play(rifle_sound)
                    ennemy_closest.hit(self.proba_tir_reussi,"t")
                    self.ammo -= 1
                    return
            else :
                self.shooting = False


    def change_range(self, r):
        self.range = r

    def play_sound(self):
        pass
        """
        if not self.playing and not pygame.mixer.Channel(2).get_busy():
            vive_lempereur_sound = pygame.mixer.Sound(os.path.join("game_assets", "grenadier-vive-lempereur.mp3"))
            vive_lempereur_sound.set_volume(0.8)
            pygame.mixer.Channel(2).play(vive_lempereur_sound)
        if pygame.mixer.Channel(2).get_busy():
            self.playing = True
        if pygame.mixer.Channel(2).get_busy():
            self.playing = False"""

