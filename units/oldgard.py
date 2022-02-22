import math
import os

import pygame

from settings import *
from units.unit import Unit

imgs = []

for x in range(1, 9):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/waiting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE*1.3, BLOCKSIZE*1.3)))

shooting_imgs = []
for x in range(1, 11):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/shooting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE*1.3, BLOCKSIZE*1.3)))

for x in range(1,3):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE*1.3, BLOCKSIZE*1.3)))

marching_imgs = []
for x in range(1, 5):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    marching_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/marching/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE*1.3, BLOCKSIZE*1.3)))

class OldGard(Unit):
    def __init__(self, line, row, ally):
        super().__init__(line, row, ally)
        self.level = 5
        self.inRange = False
        self.range = 10 * BLOCKSIZE
        self.proba_tir_reussi = 70
        self.proba_prendre_balle = 10
        self.proba_prendre_cac = 30
        self.proba_reussire_cac = 90
        self.reload_time = 10000
        self.shooting = False
        self.reloading = False
        self.marching = False
        self.is_passing = True
        self.images = imgs[:]
        self.shooting_imgs = shooting_imgs[:]
        self.marching_imgs = marching_imgs [:]
        self.draw_shooting_imgs = False
        self.max_health = 150
        self.health = self.max_health
        self.ammo = 25
        self.name = "VielleGarde"
        self.cac = False
        self.cac_reload = 2500
        self.cac_dommages = 20
        self.cacing = False
        self.price = price_old_guard

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
            # ATTACKING WITH BAYONET
            if self.cac and ennemy_closest_distance <= BLOCKSIZE:
                self.cacing = True
                now = pygame.time.get_ticks()
                if now - self.last >= self.cac_reload:
                    self.last = now
                    knife_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/knife.mp3"))
                    knife_sound.set_volume(0.3)
                    pygame.mixer.Channel(1).play(knife_sound)
                    ennemy_closest.hit(self.proba_reussire_cac, "c")

            if self.inRange and self.ammo > 0 and not self.cac:
                now = pygame.time.get_ticks()
                self.shooting = True
                if now - self.last >= self.reload_time:
                    self.last = now
                    rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/musket.mp3"))
                    rifle_sound.set_volume(0.3)
                    # pygame.mixer.Channel(1).play(rifle_sound)
                    ennemy_closest.hit(self.proba_tir_reussi, "t")
                    self.is_passing = False
                    self.ammo -= 1

    def play_sound(self):
        pass

    def change_range(self, r):
        self.range = r
