import math
import os

import pygame
import time
from settings import *
from units.unit import Unit

imgs = [pygame.image.load(os.path.join("game_assets/misc/images/canon/reloading/" + "1.png")).convert_alpha(), \
        (BLOCKSIZE * 5, BLOCKSIZE*2)]

shooting_imgs = []
for x in range(1, 46):
    add_str = str(x)
    if x < 46:
        add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/misc/images/canon/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 4, BLOCKSIZE*1.60)))


class Canon(Unit):
    def __init__(self, line, row, ally, win):
        super().__init__(line, row, ally, win)
        self.level = 5
        self.inRange = False
        self.range = 20 * BLOCKSIZE
        self.last_time_shoot = None
        self.reloading_cac = False
        self.last_time_cac = None
        self.reload_time = 10000
        self.shooting = False
        self.marching = False
        self.is_passing = True
        self.images = imgs[:]
        self.shooting_imgs = shooting_imgs[:]
        self.img = None
        self.max_health = 150
        self.health = self.max_health
        self.ammo = 25
        self.name = "Canon"
        self.cac = False
        self.cac_dommages = 20
        self.cacing = False
        self.reloading = False
        self.price = price_canon

    def attack(self, ennemies):
        self.inRange = False
        self.spawn_ball = False
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
            if ennemy_closest_distance > BLOCKSIZE:
                self.cacing = False
        if self.ammo <= 0:
            self.cac = True
        if not ennemy_closest:
            self.shooting = False

        if ennemy_closest:
            # Shooting
            if self.reloading and pygame.time.get_ticks() - self.last_time_shoot > self.reload_time + 200*10 :  # 1000
                self.reloading = False

            if self.inRange and self.ammo > 0 and not self.cac and not self.reloading:
                now = pygame.time.get_ticks()
                self.shooting = True
                self.is_passing = False
                self.ammo -= 1
                self.last_time_shoot = now
                self.reloading = True
                # ennemy_closest.hit(0, "can")
                return

    def play_sound_shooting(self):

        self.spawn_ball = True
        rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/canon.mp3"))
        rifle_sound.set_volume(0.1)
        pygame.mixer.Channel(self.channel).play(rifle_sound)

    def change_range(self, r):
        self.range = r
