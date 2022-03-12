import math
import os

import pygame
import time
from settings import *
from units.unit import Unit

## IMAGES

imgs_passive = []
timer_passive = []
for x in range(1, 9):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    imgs_passive.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/waiting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    timer_passive.append(200
                         )
aiming_imgs = []
aiming_timer = []
for x in range(1, 6):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    aiming_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/shooting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    aiming_timer.append(200)

shooting_imgs = []
shooting_timer = []
for x in range(6, 11):
    add_str = str(x)
    add_str = add_str
    shooting_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/shooting/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    shooting_timer.append(200)

reloading_imgs = []
reloading_timer = []
for x in range(1, 3):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    reloading_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/reloading/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    reloading_timer.append(5000)

imgs_marche = []
timer_marche = []
for x in range(1, 5):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    imgs_marche.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/marching/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    timer_marche.append(200)
dying_imgs = []
dying_timer = []
for x in range(2, 4):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    dying_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join("game_assets/infantry/images/vielle_garde/dying/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    dying_timer.append(1000)

marching_bayonet_imgs = []
marching_bayonet_timer = []
for x in range(5, 9):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    marching_bayonet_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join(
                "game_assets/infantry/images/vielle_garde/bayonet_marching/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))
    marching_bayonet_timer.append(200)

attacking_bayonet_imgs = []
attacking_bayonet_timer = []
for x in range(1, 7):
    add_str = str(x)
    if x < 10:
        add_str = add_str
    attacking_bayonet_imgs.append(pygame.transform.scale(
        pygame.image.load(
            os.path.join(
                "game_assets/infantry/images/vielle_garde/bayonet_attacking/" + add_str + ".png")).convert_alpha(),
        (BLOCKSIZE * 1.5, BLOCKSIZE * 1.5)))

    attacking_bayonet_timer.append(200)


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
        self.reload_time = 5000
        self.shooting = False
        self.finished_animation = None
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
            "death": dying_imgs,

        }
        self.timers = {
            "passive": timer_passive,
            "marche": timer_marche,
            "marche_bayonet": marching_bayonet_timer,
            "prepa_fusil_tir": aiming_timer,
            "fusil_tir": shooting_timer,
            "attack_bayonet": attacking_bayonet_timer,
            "recha_fusil_tir": reloading_timer,
            "death": dying_timer,
        }
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

    def attack(self, ennemies, pos):
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
        print(self.finished_animation)
        if ennemy_closest:
            # Bayonet attack
            if self.cac  and ennemy_closest_distance <= BLOCKSIZE:
                self.cacing = True
                self.reloading_cac = True
                self.is_passing = False

                # Aiming :
                if self.finished_animation == "attack_bayonet":
                    self.finished_animation = None

                    self.play_sound_bayonet()
                    ennemy_closest.hit(self.proba_tir_reussi, "c")
                    self.reloading_cac = False
                    return
                else:
                    self.behave = "attack_bayonet"
                    return
            # Shooting
            if self.finished_animation == "recha_fusil_tir":
                self.reloading = False
            if self.inRange and self.ammo > 0 and not self.cac and not self.reloading:
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
                    ennemy_closest.hit(self.proba_tir_reussi, "t")
                    return
                if self.finished_animation == "recha_fusil_tir":
                    self.behave = "prepa_fusil_tir"
                    return
                else:
                    self.behave = "prepa_fusil_tir"
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
