import math
import os

import pygame
import time
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
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))

shooting_imgs = []
for x in range(1, 11):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/shooting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))

for x in range(1, 3):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))

marching_imgs = []
for x in range(1, 5):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    marching_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/marching/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
dying_imgs = []
for x in range(2, 4):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    dying_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/dying/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))

marching_bayonet_imgs = []
for x in range(5, 9):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    marching_bayonet_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join(
                "game_assets/infantry/images/vielle_garde/bayonet_marching/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
attacking_bayonet_imgs = []
for x in range(1, 7):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    attacking_bayonet_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join(
                "game_assets/infantry/images/vielle_garde/bayonet_attacking/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))


class OldGard(Unit):
    def __init__(self, line, row, ally, win):
        super().__init__(line, row, ally, win)
        self.level = 5
        self.inRange = False
        self.range = 10 * BLOCKSIZE
        self.proba_tir_reussi = 70
        self.last_time_shoot = None
        self.reloading_cac = False
        self.last_time_cac = None
        self.proba_prendre_balle = 10
        self.proba_prendre_cac = 30
        self.proba_reussire_cac = 90
        self.reload_time = 15000
        self.shooting = False
        self.marching = False
        self.is_passing = True
        self.images = imgs[:]
        self.shooting_imgs = shooting_imgs[:]
        self.marching_imgs = marching_imgs[:]
        self.dying_imgs = dying_imgs[:]
        self.marching_bayonet_imgs = marching_bayonet_imgs[:]
        self.attacking_bayonet_imgs = attacking_bayonet_imgs[:]
        self.max_health = 200
        self.health = self.max_health
        self.ammo = 25
        self.name = "VielleGarde"
        self.cac = False
        self.cac_reload = 2500
        self.cac_dommages = 20
        self.cacing = False
        self.reloading = False
        self.price = price_old_guard

    def attack(self, ennemies):
        self.inRange = False
        ennemy_closest_distance = False
        distances = []
        ennemy_closest = None
        # Shooting
        if self.reloading and pygame.time.get_ticks() - self.last_time_shoot > self.reload_time + 2500:  # 1000
            self.reloading = False
            # ATTACKING WITH BAYONET
        if self.reloading_cac and pygame.time.get_ticks() - self.last_time_cac > self.cac_reload + 2000:  # 1000
            self.reloading_cac = False
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
                if self.cac :
                    self.accel = 1+ 10/(ennemy_closest_distance /(BLOCKSIZE))
            if ennemy_closest_distance >BLOCKSIZE :
                self.cacing = False
        if self.ammo <= 0:
            self.cac = True
        if not ennemy_closest:
            self.shooting = False
            self.cacing=False


        if ennemy_closest:
            if self.cac and not self.reloading_cac and ennemy_closest_distance <= BLOCKSIZE:
                now = pygame.time.get_ticks()
                self.cacing = True
                self.is_passing = False
                self.last_time_cac = now
                self.reloading_cac = True
                ennemy_closest.hit(self.proba_tir_reussi, "c")
                return

            if self.inRange and self.ammo > 0 and not self.cac and not self.reloading:
                now = pygame.time.get_ticks()
                self.shooting = True
                self.is_passing = False
                self.ammo -= 1
                self.last_time_shoot = now
                self.reloading = True
                ennemy_closest.hit(self.proba_tir_reussi, "t")
                return

    def play_sound_shooting(self):
        rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/musket.mp3"))
        rifle_sound.set_volume(0.1)
        pygame.mixer.Channel(self.channel).play(rifle_sound)

    def play_sound_bayonet(self):
        knife_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/knife.mp3"))
        knife_sound.set_volume(0.3)
        pygame.mixer.Channel(self.channel).play(knife_sound)

    def change_range(self, r):
        self.range = r
