import dataclasses
import os
import sched
import time
import numpy as np
import pygame
import sys
from menu.menu import VerticalMenu
from settings import *
from units import unit
from units.anglais import Anglais
from units.canon import Canon
from units.conscript import Conscript
from units.voltigeur import Voltigeur
from units.line_infantry import LineInfantry
from units.grenadier import Grenadier
from units.young_guard import YoungGuard
from units.med_guard import MedGuard
from units.oldgard import OldGard
from global_images import *

pygame.font.init()
pygame.init()


def get_line_col(x, y):
    line = round(y) // BLOCKSIZE
    row = round(x) // BLOCKSIZE
    if row <= 60 and line <= 14:
        return int(line), int(row)
    return False


def generate_mat(rows, lines):
    #
    mat = [[0 for _ in range(rows)] for _ in range(lines)]
    for r in range(rows):
        for l in range(lines):
            if r < 6 or rows - r < 6:
                mat[l][r] = -1
            if r == 20 and l == 10:
                mat[l][r] = 3
    return mat


class Game:
    def __init__(self, win):
        # VARS about screen :
        self.screen = win

        # get the default size
        self.width, self.height = win.get_size()
        # Background
        self.bg = pygame.image.load(os.path.join("game_assets", "misc/images/bg.jpeg"))
        self.bg = pygame.transform.scale(self.bg, (4000, self.height))
        # Dimensions of the matrix :
        self.lines = LIGNES
        self.rows = COLONNES
        self.MAT = generate_mat(self.rows, self.lines)
        # Global values of the player :

        # List of enemies and units on the battle field :
        self.enemies = []
        self.allies = []
        # Main menu buttons :

        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_unit, "buy_unit")
        self.menu.add_btn(tree, "Tree")
        self.moving_object = None
        self.money = 150
        self.round = bool
        self.pause = True
        self.unit_menu = None
        self.selected_units = unit

        self.lines_font = pygame.font.SysFont("comicsans", 65)
        self.lower_font = pygame.font.SysFont("comicsans", 30)
        self.wave = 0
        self.phase = 0
        pygame.display.set_caption('Napoleon Defense')

        self.time = 0

        self.clock = pygame.time.Clock()

        self.selected_unit_to_buy = None
        self.selected_unit = None
        self.upgrades = []
        self.line = 0
        self.row = 0

        self.tree = None
        self.unit_to_buy_menu = None

    def run(self):
        @dataclasses.dataclass
        class Position:
            x = 0
            y = 0

        self.scroll = Position()
        music = pygame.mixer.Sound(os.path.join("game_assets", "misc/sounds/music.mp3"))
        music.set_volume(0.5)
        # pygame.mixer.Channel(0).play(music, loops=-1)

        generated = False
        run = True
        clock = pygame.time.Clock()
        rect = pygame.Rect(0, 600, 100, 100)
        self.rect = rect
        self.rect.x = 1500

        while run:
            clock.tick(FPS)
            self.time = pygame.time.get_ticks()
            pos = pygame.mouse.get_pos()
            if pygame.time.get_ticks() > 5000:
                if not generated:
                    self.gen_army()
                    generated = True
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    run = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:

                    if self.rect.x + 100 <= 2000:
                        self.rect.x += 100
                if keys[pygame.K_LEFT]:

                    if self.rect.x - 100 >= 0:
                        self.rect.x -= 100

                # Deployment phase
                if pygame.time.get_ticks():
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.selected_unit_to_buy:
                            get_line_col(pos[0], pos[1])
                            if event.button == 1:
                                ally = True
                            else:
                                ally = False

                            if self.check_free(get_line_col(pos[0], pos[1])[0],
                                               get_line_col(pos[0], pos[1])[1]):
                                self.Add_unit(self.selected_unit_to_buy, ally, get_line_col(pos[0], pos[1])[0],
                                              get_line_col(pos[0], pos[1])[1])
                unit_to_buy = None
                tree_menu_button = None
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if get_line_col(pos[0], pos[1]):
                        l, c = \
                            get_line_col(pygame.mouse.get_pos()[0] + self.rect.x,
                                         pygame.mouse.get_pos()[1] - BLOCKSIZE)[0], \
                            get_line_col(pygame.mouse.get_pos()[0] + self.rect.x,
                                         pygame.mouse.get_pos()[1] - BLOCKSIZE)[1]
                        self.line = l
                        self.row = c
                        # SELECT UNIT ON THE BOARD TO BUY
                        self.selected_unit = self.detect_select_unit()
                    if self.menu: side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                    if self.tree: tree_menu_button = self.tree.get_clicked(pos[0], pos[1])
                    if self.unit_to_buy_menu: unit_to_buy = self.unit_to_buy_menu.get_clicked(pos[0], pos[1])
                    if side_menu_button:
                        if str(side_menu_button) == "Tree":
                            self.open_tree()
                            break
                        if str(side_menu_button) == "buy_unit":
                            self.open_units_by()
                            break
                    if tree_menu_button:
                        if str(tree_menu_button) == "close":
                            self.tree = None
                            break
                    if unit_to_buy:
                        if str(unit_to_buy) == "close":
                            self.unit_to_buy_menu = None
                            break
                        if str(unit_to_buy):
                            cost = self.menu.get_item_cost(unit_to_buy)
                            if self.money >= cost:
                                self.selected_unit_to_buy = unit_to_buy
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    if self.unit_menu:
                        unit_button = self.unit_menu.get_clicked(pos[0], pos[1])
                        if self.selected_unit:
                            if unit_button:
                                pass
                                # Open the tree

                                # self.upgrade_unit(self.selected_unit)

                if event.type == pygame.KEYDOWN:
                    if self.selected_unit:
                        # BAYONET MODE
                        if event.key == pygame.K_b:
                            if not self.selected_unit.cac:
                                self.selected_unit.cac = True
                            else:
                                self.selected_unit.cac = False
                        # LEVEL UP
                        if event.key == pygame.K_l:
                            self.upgrade_unit(self.selected_unit)

            # MOVING ALL UNITS IN THE BATTLE FIELD
            unites = []
            for k in range(len(self.enemies) + len(self.allies)):
                if k < len(self.enemies):
                    unites.append(self.enemies[k])
                if k < len(self.allies):
                    unites.append(self.allies[k])

            for element in unites:
                if element.is_dead:
                    if element.ally:
                        self.allies.remove(element)
                        break
                    else:
                        self.enemies.remove(element)
                        break
                if element.health <= 0:
                    break
                if element.ally:
                    if self.MAT[element.line][element.row+1] == 0 :
                        element.move(self.MAT, self.enemies)
                else:
                    element.move(self.MAT, self.allies)

                self.update_single_mat(element)

                if self.MAT[element.line][element.row - 8] == 0:
                    if element.ally:
                        element.attack(self.enemies)
                    else:
                        element.attack(self.allies)

            self.update_mat(unites)
            self.draw()
        pygame.quit()

    def open_tree(self):
        """
            Open tree
        """
        self.tree = VerticalMenu(self.width / 2, 180, tree_image)
        self.create_tree()

    def open_units_by(self):
        self.unit_to_buy_menu = VerticalMenu(self.width / 2, 180, tree_image)
        self.create_unit_to_buy_menu()

    def create_unit_to_buy_menu(self):
        self.unit_to_buy_menu.add_btn(close, "close")
        self.unit_to_buy_menu.add_btn(Conscript_img, "Conscript")
        if "LineInfantry" in self.upgrades:
            self.unit_to_buy_menu.add_btn(LineInfantry_img, "LineInfantry", 500)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(Grenadier_img, "Grenadier", 2300)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(YoungGuard_img, "YoungGuard", 1500)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(MedGuard_img, "MedGuard", 2300)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(OldGuard_img, "OldGuard", 4000)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(Chasseur_img, "Chasseur", 800)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(Flanqueur_img, "Flanqueur", 1200)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(GuardChasseur_img, "GuardChasseur", 2000)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(Volitgeur_img, "Voltigeur", 2900)
        if "Grenadier" in self.upgrades:
            self.unit_to_buy_menu.add_btn(GuardVoltigeur_img, "GuardVoltigeur", 4000)

    def create_tree(self):

        self.tree.add_btn(close, "close")
        self.tree.add_btn(Conscript_img, "Conscript")
        self.tree.add_btn(LineInfantry_img, "LineInfantry", 500)
        self.tree.add_btn(Grenadier_img, "Grenadier", 1000)
        self.tree.add_btn(YoungGuard_img, "YoungGuard", 1500)
        self.tree.add_btn(MedGuard_img, "MedGuard", 2300)
        self.tree.add_btn(OldGuard_img, "OldGuard", 4000)
        self.tree.add_btn(Chasseur_img, "Chasseur", 800)
        self.tree.add_btn(Flanqueur_img, "Flanqueur", 1200)
        self.tree.add_btn(GuardChasseur_img, "GuardChasseur", 2000)
        self.tree.add_btn(Volitgeur_img, "Voltigeur", 2900)
        self.tree.add_btn(GuardVoltigeur_img, "GuardVoltigeur", 4000)

    def draw(self):
        """
        Draw all elements on the screen
        :return: None
        """
        phase = False
        if self.selected_unit_to_buy:
            phase = True
        self.screen.blit(self.bg, (-self.rect.x, 0))

        self.drawGrid(phase)
        self.draw_hover()
        if self.selected_unit:
            self.unit_menu = VerticalMenu(self.width - side_img.get_width() + 70, 800, unit_menu_img)
            self.selected_unit.draw_selected_unit(self.screen, self.rect.x)
            self.unit_menu.add_btn(bayonet, "bayonet")
            self.unit_menu.add_btn(scope, "scope")
            self.unit_menu.add_btn(special, "special")
            # DO ACTION WHEN SELECTED UNIT
        for en in self.enemies:
            en.draw(self.screen, self.rect.x)
            # en.draw_health_bar(self.screen, self.rect.x)

        for element in self.allies:
            element.draw(self.screen, self.rect.x)
            # element.draw_health_bar(self.screen,self.rect.x)

        # draw unit_menu
        if self.unit_menu:
            self.unit_menu.draw(self.screen)
        # draw tree
        if self.tree:
            self.tree.draw(self.screen)

        if self.unit_to_buy_menu:
            self.unit_to_buy_menu.draw(self.screen)
        # draw menu , money
        self.menu.draw(self.screen)
        text = self.lines_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(money_img, (50, 50))
        start_x = self.width - 50 - 10

        self.screen.blit(text, (start_x - text.get_width() - 10, 75))
        self.screen.blit(money, (start_x, 65))

        # draw clock

        timer = self.lower_font.render(str(round(pygame.time.get_ticks() / 1000, 1)), 1, (255, 0, 0))
        clock = pygame.transform.scale(clock_img, (30, 30))
        self.screen.blit(timer, (self.width - text.get_width(), 20))
        self.screen.blit(clock, (self.width - text.get_width() - 50, 20))

        pygame.display.update()

    def Add_unit(self, name, ally, line, col):
        """
        Add a unit and add it to the list of enemies or unit
        :param name: name of the unit used to identify it
        :param ally: if unit is on player side or not
        :param line: position of the unit (y)
        :param col: position of the unit (x)
        """
        element = None
        if ally:
            if col < 60:
                if self.MAT[line][col] == 0:
                    if name == "buy_old_gard":
                        element = OldGard(line, col, ally, self.screen)
                        self.allies.append(element)
                    if name == "buy_voltigeur":
                        element = Voltigeur(line, col, ally, self.screen)
                        self.allies.append(element)
                    if name == "buy_canon":
                        element = Canon(line, col, ally, self.screen)
                        self.allies.append(element)
        if not ally:
            if self.MAT[line][col] == 0:
                if name == "buy_old_gard":
                    element = OldGard(line, col, ally, self.screen)
                    self.enemies.append(element)
                if name == "buy_voltigeur":
                    element = Voltigeur(line, col, ally, self.screen)
                    self.enemies.append(element)
        if element:
            self.money -= element.price
            self.update_single_mat(element)
            self.selected_unit_to_buy = None

    def check_free(self, x, y):
        try:
            if self.MAT[x][y] == 0:
                return True
            return False
        except IndexError:
            pass

    def update_single_mat(self, element):
        unit_line = element.x
        unit_row = element.y
        line, row = get_line_col(unit_line, unit_row)

        self.MAT[line][row] = element.slug

    def update_mat(self, units):
        self.MAT = generate_mat(self.rows, self.lines)
        for element in units:
            unit_line = element.x
            unit_col = element.y
            line, col = get_line_col(unit_line, unit_col)
            print("UNIT {} at {} {}".format(element.name, line, col))
            self.MAT[line][col] = element.slug

    def drawGrid(self, phase):
        blksize = BLOCKSIZE  # Set the size of the grid block
        # GET grid size :
        for x in range(self.rows):
            for y in range(self.lines):
                rect = pygame.Rect(x * blksize - self.rect.x, y * blksize + blksize,
                                   blksize, blksize)
                if self.MAT[y][x] == 0:
                    pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.MAT[y][x] == -1:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                # ARBRE
                if self.MAT[y][x] == 3:
                    pygame.draw.rect(self.screen, (0, 200, 0), rect, 0)
                    #self.screen.blit(tree_land, (rect.x, rect.y))
                else :
                    slug = self.MAT[y][x]
                    unit = find_unit_with_slug(self.enemies+self.allies,slug)
                    if unit :
                        if unit.ally :
                            pygame.draw.rect(self.screen, (0, 200, 0), rect, 0)
                        if not unit.ally :
                            pygame.draw.rect(self.screen, (200, 0, 0), rect, 0)

        if phase:
            for x in range(self.rows):
                for y in range(self.lines):

                    rect = pygame.Rect(x * blksize, y * blksize,
                                       blksize, blksize)
                    if x < 4:
                        pygame.draw.rect(self.screen, (0, 200, 0), rect, 2)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_hover(self):
        pos = pygame.mouse.get_pos()

        if get_line_col(pos[0], pos[1]):
            l, c = get_line_col(pygame.mouse.get_pos()[0] + self.rect.x, pygame.mouse.get_pos()[1] - BLOCKSIZE)[0], \
                   get_line_col(pygame.mouse.get_pos()[0] + self.rect.x, pygame.mouse.get_pos()[1] - BLOCKSIZE)[1]
            slug = None
            if c <= 60 and l <= 25:
                slug = self.MAT[l][c]

                unit_hovered = find_unit_with_slug(self.enemies + self.allies, slug)
            if unit_hovered:
                unit_hovered.draw_radius(self.screen, self.rect.x)
                # unit_hovered.draw_health_bar(self.screen,self.rect.x)
                unit_hovered.draw_info(self.screen, self.rect.x)
                # self.rows licks.append(pos)

    def detect_select_unit(self):
        try:
            line, row = self.line, self.row
            if line <= LIGNES and row <= COLONNES:
                slug = self.MAT[line][row]
                unit_selected = find_unit_with_slug(self.enemies + self.allies, slug)
                if unit_selected and unit_selected.ally:
                    return unit_selected
            return None
        except IndexError:
            pass

    def upgrade_unit(self, element):
        """
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
        :param element:
        :return:
        """
        # Upgrade conscript to line infantry
        try:
            self.selected_unit = None
            if element.level == 0:
                unit_leveled_up = LineInfantry(element.line, element.row, element.ally)
                self.allies.append(unit_leveled_up)
                self.allies.remove(element)
                return
            # Upgrade line infantry to grenadier
            if element.level == 1:
                unit_leveled_up = Grenadier(element.line, element.row, element.ally)
                self.allies.append(unit_leveled_up)
                self.allies.remove(element)
                return
            # Upgrade grenadier to young guard
            if element.level == 2:
                unit_leveled_up = MedGuard(element.line, element.row, element.ally)
                self.allies.append(unit_leveled_up)
                self.allies.remove(element)
                return
            # Upgrade young guard to med guard
            if element.level == 3:
                unit_leveled_up = YoungGuard(element.line, element.row, element.ally)
                self.allies.append(unit_leveled_up)
                self.allies.remove(element)
                return
            # Upgrade med guard to old guard
            if element.level == 4:
                unit_leveled_up = OldGard(element.line, element.row, element.ally)
                self.allies.append(unit_leveled_up)
                self.allies.remove(element)
                return
        except Exception as e:
            pass

    def gen_army(self):

        self.Add_unit("buy_old_gard", True, 8, 7)
        self.Add_unit("buy_old_gard", True, 8, 6)
        self.Add_unit("buy_old_gard", False, 8, 40)
        """
        self.Add_unit("buy_old_gard", False, 4, 40)
        self.Add_unit("buy_old_gard", False, 5, 40)
        self.Add_unit("buy_old_gard", False, 6, 40)
        self.Add_unit("buy_old_gard", False, 7, 40)
        self.Add_unit("buy_old_gard", False, 8, 40)
        self.Add_unit("buy_old_gard", False, 9, 40)"""

        #self.Add_unit("buy_old_gard", True, 1, 6)
        #self.Add_unit("buy_voltigeur", True, 1, 7)
        """self.Add_unit("buy_old_gard", True, 3, 1)
        self.Add_unit("buy_old_gard", True, 4, 1)
        self.Add_unit("buy_old_gard", True, 5, 1)
        self.Add_unit("buy_old_gard", True, 1, 2)
        self.Add_unit("buy_old_gard", True, 2, 2)
        self.Add_unit("buy_old_gard", True, 3, 2)
        self.Add_unit("buy_old_gard", True, 4, 2)
        self.Add_unit("buy_old_gard", True, 5, 2)
        self.Add_unit("buy_voltigeur", True, 1, 3)
        self.Add_unit("buy_voltigeur", True, 2, 3)
        self.Add_unit("buy_voltigeur", True, 3, 3)
        self.Add_unit("buy_voltigeur", True, 4, 3)
        self.Add_unit("buy_voltigeur", True, 5, 3)

        self.Add_unit("buy_old_gard", True, 6,1)
        self.Add_unit("buy_old_gard", True, 7, 1)
        self.Add_unit("buy_old_gard", True, 8, 1)
        self.Add_unit("buy_old_gard", True, 9, 1)"""


def find_unit_with_slug(units, slug):
    for element in units:
        if element.slug == slug:
            return element
        else:
            pass
    return None
