import math
import os
import random
import string

import pygame

from settings import *


def get_path(ally, ligne, colonne):
    lignes = LIGNES
    colonnes = COLONNES
    all_path = []
    for l in range(lignes):
        new_path = []
        for c in range(colonnes):
            if ally and c * BLOCKSIZE > 500:
                new_path.append((c * BLOCKSIZE, l * BLOCKSIZE))
            if not ally and c * BLOCKSIZE < 3500:
                new_path.append((c * BLOCKSIZE, l * BLOCKSIZE))
        all_path.append(new_path)
    if ally:
        return all_path[ligne][colonne:]
    else:
        return all_path[ligne][colonnes - colonne:]


class Unit:
    channel = 1

    def __init__(self, line, row, ally, win, width=65, height=65, velocity=3):
        self.channel = Unit.channel
        Unit.channel += 1
        self.lines_font = pygame.font.SysFont("comicsans", 30)
        self.shooting = False
        self.cacing = False
        self.name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.spawn_ball = False
        self.line = line
        self.row = row
        self.ally = ally
        self.x = row * BLOCKSIZE
        self.y = line * BLOCKSIZE
        self.path = []
        self.path_pos = 0
        self.move_count = 0
        self.dis = 0
        self.lastReloadTime = 0
        self.proba_prendre_balle = 0
        self.proba_prendre_cac = 0
        self.level = None
        self.playing = False
        self.img = {}
        self.win = win
        self.shooting_imgs = []
        self.shooting_img = False
        self.marching = False
        self.reloading = False
        self.pattern = False
        self.begin_death = False
        self.spawn_ball = False
        self.accel = 2
        self.marching_imgs = []
        self.reloading_imgs = []
        self.dying_imgs = []
        self.images = None
        self.font = pygame.font.SysFont("franklingothicmedium", 25)
        self.slug = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.animation_count = 0
        self.width = width
        self.height = height
        self.range = 0
        self.max_health = 10
        self.health = 10
        self.reload_time = 10000
        self.is_dead = False
        self.flipped = False
        self.halt_fire = False
        self.timer_animation = pygame.time.get_ticks()
        self.timer_reloading = pygame.time.get_ticks()
        self.timer_death_animation = pygame.time.get_ticks()
        self.upgrade_cost = {"price_conscript": price_conscript,
                             "price_line_infantry": price_line_infantry,
                             "price_grenadier": price_grenadier,
                             "price_young_guard": price_young_guard,
                             "price_med_guard": price_med_guard,
                             "price_old_guard": price_old_guard,
                             "price_chasseur": price_chasseur,
                             "price_fanqueur": price_fanqueur,
                             "price_guard_chasseur": price_guard_chasseur,
                             "price_voltigeur": price_voltigeur,
                             "price_guard_voltigeur": price_guard_voltigeur}
        self.sell_price = [1, 2, 3, 4, 5]
        self.selected = False
        self.menu = ""
        self.enemies = []

        self.hover = False
        self.behave = "passive"
        self.finished_animation = False

    def draw(self, surface, pos):
        """
        draw the unit with the given images
        :param surface: surface
        :return: None
        """

        if self.finished_animation =="death":
            self.is_dead = True
        if not self.is_dead:
            self.draw_health_bar(surface, pos)
            self.play_animation(surface, pos, self.behave)


    def draw_radius(self, win, pos):
        if self.name == "Canon":
            pygame.draw.circle(win, (255, 0, 0), (self.x - pos, self.y), self.range, 10)
        else:
            pygame.draw.circle(win, (255, 0, 0), (self.x - pos, self.y), self.range, 1)

    def draw_selected_unit(self, win, pos):
        text = self.font.render(str(self.ammo), 1, (255, 255, 255))
        # canon_ball = pygame.image.load(os.path.join("game_assets", "ball.png"))
        # img = pygame.transform.scale(canon_ball, (20, 20))

        win.blit(text, (self.x + 3 - pos, self.y + 5))

    def draw_info(self, win, pos):
        pass

    def draw_health_bar(self, win, pos):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        pygame.draw.rect(win, (255, 0, 0), (self.x - pos, self.y - 10, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - pos, self.y - 10, health_bar, 10), 0)

    def move(self, mat, ennemies):
        """
        Move enemy
        :return: None
        """
        if self.name == "Canon": return
        if not self.path:

            if self.ally:
                self.path = get_path(self.ally, self.line, self.row)
            else:
                self.path = get_path(self.ally, self.line, self.row)[::-1]
        try:
            if not self.shooting and not self.cacing:
                x1, y1 = self.path[self.path_pos]

                if self.path_pos + 1 >= len(self.path):
                    self.path = []
                    self.path_pos = 0
                    return
                x2, y2 = self.path[self.path_pos + 1]

                if not check_free(mat, x2, y2): return
                if True:
                    dirn = ((x2 - x1), (y2 - y1))
                    length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2) * 1 / self.accel
                    if length == 0:
                        length = 0.0001
                    dirn = (dirn[0] / length, dirn[1] / length)
                    if dirn[0] < 0 and not (self.flipped):
                        self.flipped = True
                    if dirn[0] > 0 and self.flipped:
                        self.flipped = False
                    move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
                    if self.cac:
                        self.behave = "marche_bayonet"
                    else:
                        self.behave = "marche"
                    self.x = move_x
                    self.y = move_y
                    self.marching = True
                    ligne, col = int(self.y // BLOCKSIZE), int(self.x // BLOCKSIZE)
                    self.line = ligne
                    self.row = col

                    # Go to next point
                    if dirn[0] >= 0:  # moving right
                        if dirn[1] >= 0:  # moving down
                            if self.x >= x2 and self.y >= y2:
                                self.path_pos += 1
                        else:
                            if self.x >= x2 and self.y <= y2:
                                self.path_pos += 1
                    else:  # moving left
                        if dirn[1] >= 0:  # moving down
                            if self.x <= x2 and self.y >= y2:
                                self.path_pos += 1
                        else:
                            if self.x <= x2 and self.y >= y2:
                                self.path_pos += 1
        except:
            pass

    def add_point(self, line, col):
        xf = col * BLOCKSIZE
        yf = line * BLOCKSIZE
        posx = self.x
        posy = self.y
        self.path = []
        path = [(posx, posy)]
        distance = math.sqrt((posx - xf) ** 2 + (posy - yf) ** 2)
        for i in range(int(distance / BLOCKSIZE)):
            if xf - posx < 0:
                posx = posx - BLOCKSIZE
            if xf - posx > 0:
                posx = posx + BLOCKSIZE
            if yf - posy < 0:
                posy = posy - BLOCKSIZE
            if yf - posy > 0:
                posy = posy + BLOCKSIZE
            path.append((posx, posy))
        self.path = path

    def hit(self, proba_touche, type):
        """
        returns if unit has died
        :return:
        """
        dommages_balle = 6
        dommages_bayonet = 10
        if type == "c": self.cac = True
        self.health -= 70

        print("shoot", type)
        if type == "can":
            self.health -= 500
        if self.health <= 0:
            self.behave = "death"
            return True
        return False

    def add_closest_ennemy_to_path(self, ennemies):
        ennemy_closest_distance = False
        distances = []
        ennemy_closest = None
        path = []
        for ennemy in ennemies:
            ennemy_x, ennemy_y = ennemy.x, ennemy.y
            dis = math.sqrt((self.x - ennemy_x) ** 2 + (self.y - ennemy_y) ** 2)
            distances.append(dis)
        if distances:
            ennemy_closest_distance = min(distances)
            index_closest = distances.index(ennemy_closest_distance)
            ennemy_closest = ennemies[index_closest]
            xf = ennemy_closest.x
            yf = ennemy_closest.y
            posx = self.x
            posy = self.y
            path = [(posx, posy)]
            for i in range(int(ennemy_closest_distance / BLOCKSIZE)):
                if xf - posx < 0:
                    posx = posx - BLOCKSIZE
                if xf - posx > 0:
                    posx = posx + BLOCKSIZE
                if yf - posy < 0:
                    posy = posy - BLOCKSIZE
                if yf - posy > 0:
                    posy = posy + BLOCKSIZE
                path.append((posx, posy))
            self.path = path

    def play_animation(self, surface, pos, name):
        now = pygame.time.get_ticks()
        imgs_array = self.get_imgs(name)
        timer_array = self.get_timer_array(name)

        if self.animation_count >= len(timer_array):
            self.animation_count = 0
        if now - self.timer_animation >= timer_array[self.animation_count]:
            self.timer_animation = now
            self.animation_count += 1
        if self.animation_count >= len(imgs_array):
            self.animation_count = 0
            self.finished_animation = self.behave
        self.img = imgs_array[self.animation_count]
        if self.flipped:
            self.img = pygame.transform.flip(self.img, True, False)
        surface.blit(self.img, (self.x - BLOCKSIZE - pos, self.y + 0.5 * BLOCKSIZE))

    def get_imgs(self, name):
        return self.imgs[name]

    def get_timer_array(self, name):
        return self.timers[name]


def check_free(mat, x, y):
    l, c = int(y // BLOCKSIZE), int(x // BLOCKSIZE)
    if mat[l][c] == 0:
        return True
    return True
