import pygame
import math
import os
import time
from settings import *
import string
import random


class Unit:
    channel = 1

    def __init__(self, line, row, ally, win, width=65, height=65, velocity=3):
        self.channel = Unit.channel
        Unit.channel += 1
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
        self.win = win
        self.shooting_imgs = []
        self.shooting_img = False
        self.marching = False
        self.reloading = False
        self.begin_death = False
        self.marching_imgs = []
        self.reloading_imgs = []
        self.dying_imgs = []
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
        self.reload_time = 10000
        self.is_dead = False
        self.flipped = False
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

    def draw(self, surface):
        """
        draw the unit with the given images
        :param surface: surface
        :return: None
        """

        if self.is_dead:
            return
        now = pygame.time.get_ticks()

        # dying
        if self.health <= 0 and not self.is_dead:
            dying_timer_array = [1600, 1000, 500]
            if not self.begin_death:
                    self.animation_count = 0
                    self.begin_death = True

            if now - self.timer_animation >= dying_timer_array[self.animation_count]:
                self.timer_animation = now
                self.animation_count += 1

            if self.animation_count >= len(self.dying_imgs):
                self.is_dead = True
                return

            self.img = self.dying_imgs[self.animation_count]
            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            surface.blit(self.img, (self.x, self.y))
            return

        # shooting
        if self.shooting:
            shooting_timer_table = [200, 200, 200, 200, 100, 100, 100, 100, 100, 300, 300, self.reload_time]
            if now - self.timer_animation >= shooting_timer_table[self.animation_count]:
                self.timer_animation = now
                self.animation_count += 1

            if self.animation_count >= len(self.shooting_imgs) + len(self.reloading_imgs):
                self.animation_count = 0
            self.shooting_imgs += self.reloading_imgs
            if self.animation_count == 8:
                self.play_sound_shooting()
            self.img = self.shooting_imgs[self.animation_count]
            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            surface.blit(self.img, (self.x, self.y))
            # Smoke effect
            img = pygame.image.load(os.path.join("game_assets", "infantry/images/smoke1.png"))
            img = pygame.transform.scale(img, (30, 40))

            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            surface.blit(img, (self.x, self.y))
            return

        # marching

        if self.marching and not self.shooting:
            marching_timer_array = [300, 300, 300, 300]
            if now - self.timer_animation >= marching_timer_array[self.animation_count]:
                self.timer_animation = now
                self.animation_count += 1

            if self.animation_count >= len(self.marching_imgs):
                self.animation_count = 0
            self.img = self.marching_imgs[self.animation_count]

            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            surface.blit(self.img, (self.x, self.y))
            return

        # Passive
        passive_timer_array = [300, 300, 300, 300, 300, 300, 300, 300]
        if now - self.timer_animation >= passive_timer_array[self.animation_count]:
            self.timer_animation = now
            self.animation_count += 1
        if not self.shooting and not self.marching:
            if self.animation_count >= len(self.images):
                self.animation_count = 0
            self.img = self.images[self.animation_count]

            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            surface.blit(self.img, (self.x, self.y))
            return

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
        self.marching = False
        if ennemies:

            self.add_closest_ennemy_to_path(ennemies)
            if not self.shooting and not self.cacing:
                x1, y1 = self.path[self.path_pos]
                if self.path_pos + 1 >= len(self.path):
                    self.path_pos = 0
                x2, y2 = self.path[self.path_pos + 1]
                if check_free(mat, x2, y2):
                    dirn = ((x2 - x1), (y2 - y1))
                    length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
                    dirn = (dirn[0] / length, dirn[1] / length)
                    if dirn[0] < 0 and not self.flipped:
                        self.flipped = True
                    move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
                    self.marching = True
                    self.x = move_x
                    self.y = move_y
                    self.ligne, self.colonne = get_line_col(self.y, self.x)

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
        self.health -= 150
        surface = self.win
        if self.health <= 0:
            return True
        return False
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


def get_line_col(x, y):
    if x % BLOCKSIZE > BLOCKSIZE / 2:
        x += x % BLOCKSIZE
    else:
        x -= x % BLOCKSIZE

    if y % BLOCKSIZE > BLOCKSIZE / 2:
        y += y % BLOCKSIZE
    else:
        y -= y % BLOCKSIZE
    line = round(y) // BLOCKSIZE
    row = round(x) // BLOCKSIZE
    return int(line), int(row)
