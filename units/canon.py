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
imgs_passive = []
timer_passive = []
for x in range(1,2):
    add_str = str(x)
    if x < 2:
        add_str = add_str
    imgs_passive.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/misc/images/canon/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 4, BLOCKSIZE*1.60)))
    timer_passive.append(200
                         )
aiming_imgs = []
aiming_timer = []
for x in range(1, 10):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    aiming_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/misc/images/canon/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 4, BLOCKSIZE*1.60)))
    aiming_timer.append(200)

shooting_imgs = []
shooting_timer = []
for x in range(11, 13):
    add_str = str(x)
    add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/misc/images/canon/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 4, BLOCKSIZE * 1.60)))
    shooting_timer.append(200)

reloading_imgs = []
reloading_timer = []
for x in range(14, 46):
    add_str = str(x)
    if x < 47:
        add_str = add_str
    reloading_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/misc/images/canon/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 4, BLOCKSIZE * 1.60)))
    if x == 34 or x==35:
        reloading_timer.append(5000)
    else :
        reloading_timer.append(200)

imgs_marche = []
timer_marche = []
dying_imgs = []
dying_timer = []
marching_bayonet_imgs = []
marching_bayonet_timer = []

attacking_bayonet_imgs = []
attacking_bayonet_timer = []

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
        self.imgs = {
            "passive": imgs_passive,
            "marche": imgs_marche,
            "marche_bayonet": marching_bayonet_imgs,
            "prepa_fusil_tir": aiming_imgs,
            "fusil_tir": shooting_imgs,
            "attack_bayonet": attacking_bayonet_imgs,
            "recha_fusil_tir": reloading_imgs,
            "death": dying_imgs,}
        self.timers = {
            "passive": timer_passive,
            "marche": timer_marche,
            "marche_bayonet": marching_bayonet_timer,
            "prepa_fusil_tir": aiming_timer,
            "fusil_tir": shooting_timer,
            "attack_bayonet": attacking_bayonet_timer,
            "recha_fusil_tir": reloading_timer,}
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

    def attack(self, ennemies,pos):
        self.inRange = False
        self.spawn_ball = False
        self.inRange = False
        ennemy_closest_distance = False
        distances = []
        ennemy_closest = None
        # Shooting
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
                if self.cac:
                    self.accel = 1 + 10 / (ennemy_closest_distance / (BLOCKSIZE))
            if ennemy_closest_distance > BLOCKSIZE:
                self.cacing = False
        if self.ammo <= 0:
            self.cac = True
        if not ennemy_closest:
            self.shooting = False
            self.cacing = False
            self.accel = 2
        if ennemy_closest:

            # Shooting
            if self.finished_animation == "recha_fusil_tir":
                self.reloading = False
            if not self.reloading:
                if self.inRange and self.ammo > 0 and not self.cac and not self.halt_fire:
                    self.shooting = True
                    self.is_passing = False
                    # Aiming :
                    if self.finished_animation == "prepa_fusil_tir":
                        self.behave = "fusil_tir"
                        return
                    if self.finished_animation == "fusil_tir":
                        self.behave = "recha_fusil_tir"

                        self.play_sound_shooting()
                        self.ammo -= 1
                        self.reloading = True
                        self.spawn_ball = True
                        return
                    if self.finished_animation == "recha_fusil_tir":
                        self.behave = "prepa_fusil_tir"

                        return
                    else:
                        self.behave = "prepa_fusil_tir"
                        return


    def play_sound_shooting(self):
        """
        rifle_sound = pygame.mixer.Sound(os.path.join("game_assets", "infantry/sounds/canon.mp3"))
        rifle_sound.set_volume(0.1)
        pygame.mixer.Channel(self.channel).play(rifle_sound)"""

    def change_range(self, r):
        self.range = r
