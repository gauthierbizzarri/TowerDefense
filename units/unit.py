import pygame
import math
import os
from settings import *
import string
import random


class Unit:
    def __init__(self, line, row, ally, width=64, height=64, velocity=3, ):
        self.shooting = False
        self.cacing = False
        self.name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        self.line = line
        self.row = row
        self.ally = ally
        self.path = [(row * BLOCKSIZE, line * BLOCKSIZE)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.move_count = 0
        self.dis = 0
        self.proba_prendre_balle = 0
        self.proba_prendre_cac = 0
        self.level = None
        self.playing = False
        self.img = []
        self.images = None
        self.font = pygame.font.SysFont("franklingothicmedium", 25)
        self.slug = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        self.animation_count = 0
        self.width = width
        self.height = height
        self.velocity = velocity
        self.range = 0
        self.max_health = 10
        self.health = 10
        self.flipped = False
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

    def draw(self, surface):
        """
        draw the unit with the given images
        :param surface: surface
        :return: None
        """
        # self.animation_count += 1

        if self.animation_count >= len(self.images):
            self.animation_count = 0
        self.img = self.images[self.animation_count]

        surface.blit(self.img, (self.x, self.y))
        # self.draw_health_bar(surface)
        if self.shooting:
            img = pygame.image.load(os.path.join("game_assets", "infantry/images/smoke.png"))
            img = pygame.transform.scale(img, (30, 40))
            surface.blit(img, (self.x, self.y))

    def draw_radius(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.range, 1)

    def draw_selected_unit(self, win):
        text = self.font.render(str(self.ammo), 1, (255, 255, 255))
        # canon_ball = pygame.image.load(os.path.join("game_assets", "ball.png"))
        # img = pygame.transform.scale(canon_ball, (20, 20))

        if self.cac:
            bayonet = pygame.image.load(os.path.join("game_assets", "infantry/images/bayonet.png"))
            bayonet = pygame.transform.scale(bayonet, (40, 40))
            win.blit(bayonet, (self.x - 50, self.y - 10))
        win.blit(text, (self.x + 3, self.y + 5))

    def draw_canon_ball(self, win):
        """img = pygame.image.load(os.path.join("game_assets", "infantry/imgs/ball.png"))
        canon = pygame.transform.scale(img, (30, 30))
        m = 1
        g = 9.81
        v0 = 250 / 3.6
        vx0 = v0 * math.cos(70)
        vy0 = v0 * math.sin(70)
        dt = 0.5
        t = 0
        x = 0
        y = 0
        vx = vx0
        vy = vy0
        while y >= 0:
            x = x + dt * vx
            y = y + dt * vy
            vx = vx + dt * vx
            vy = vy + dt * vy  - dt * g
            t = t + dt
            win.blit(canon, (self.x +x, self.y + y))"""

    def draw_info(self, win):
        pass

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        """if self.ally:
            pygame.draw.circle(win, (0, 255, 0),  (self.x+15  ,self.y - 7), 5, 0)
        else:
            pygame.draw.circle(win, (255, 0, 0),  (self.x +15 ,self.y - 7), 5, 0)"""
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 10, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 10, health_bar, 10), 0)

    def collide(self, x, y):
        """
        return if position has hit
        :param x:
        :param y:
        :return: bool
        """
        if x < self.x + self.width and x < self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def click(self, x, y):
        """
                returns if unit has been clicked on
                and selects unit if it was clicked
                :param x: int
                :param y: int
                :return: bool
                """
        img = self.images[self.level - 1]
        if x <= self.x - img.get_width() // 2 + self.width and x >= self.x - img.get_width() // 2:
            if y <= self.y + self.height - img.get_height() // 2 and y >= self.y - img.get_height() // 2:
                return True
        return False

    def sell(self):
        return self.sell_price

    def upgrade(self):
        if self.level < len(self.images):
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        return self.upgrade_cost[self.level - 1]

    def move(self, mat, ennemies):
        """
        Move enemy
        :return: None
        """
        if ennemies:
            self.add_closest_ennemy_to_path(ennemies)
            if not self.shooting and not self.cacing:
                self.animation_count += 1
                if self.animation_count >= len(self.images):
                    self.animation_count = 0

                x1, y1 = self.path[self.path_pos]
                if self.path_pos + 1 >= len(self.path):
                    self.path_pos = 0
                x2, y2 = self.path[self.path_pos + 1]
                if check_free(mat, x2, y2):
                    dirn = ((x2 - x1), (y2 - y1))
                    length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
                    dirn = (dirn[0] / length, dirn[1] / length)
                    if dirn[0] < 0 and not (self.flipped):
                        self.flipped = True
                        for x, img in enumerate(self.images):
                            self.images[x] = pygame.transform.flip(img, True, False)
                    if not self.ally:
                        pass
                    move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

                    self.x = move_x
                    self.y = move_y
                    ligne, col = int(self.y // BLOCKSIZE), int(self.x // BLOCKSIZE)
                    self.ligne = ligne
                    self.colonne = col

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

    def hit(self, proba_touche, type):
        """
        returns if unit has died
        :return:
        """
        dommages_balle = 6
        dommages_bayonet = 10
        if type == "t":
            self.health -= dommages_balle
        if type == "c":
            self.health -= dommages_bayonet
        # TEST CAC TOUCHE :
        """if type =="t":
            if randrange(101)<proba_touche:
                if randrange(101)<self.proba_prendre_balle:
                        self.health -= dommages_balle
        if type == "c":
            if randrange(101) < proba_touche:
                if randrange(101) < self.proba_prendre_cac:
                    self.health -= dommages_bayonet
        if self.health <= 0: return True
        return False"""

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


def check_free(mat, x, y):
    ligne, col = int(y // BLOCKSIZE), int(x // BLOCKSIZE)
    if mat[ligne][col] == 0:
        return True
    return False
