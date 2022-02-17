import os
import sched
import time

import pygame

from menu.menu import VerticalMenu
from settings import *
from units import unit
from units.anglais import Anglais
from units.canon import Canon
from units.conscript import Conscript
from units.line_infantry import LineInfantry
from units.grenadier import Grenadier
from units.young_guard import YoungGuard
from units.med_guard import MedGuard
from units.oldgard import OldGard

pygame.font.init()
pygame.init()

side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/board.jpeg"))
                                  .convert_alpha(), (130, 500))
unit_menu_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/board.jpeg"))
                                       .convert_alpha(), (180, 250))
star_img = pygame.image.load(os.path.join("game_assets", "misc/images/star.png")).convert_alpha()

buy_old_gard = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/viellegarde.png")).convert_alpha(), (75, 75))
buy_conscript = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/conscrit.png")).convert_alpha(), (75, 75))
buy_canon = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/canon.png")).convert_alpha(), (75, 75))

bayonet = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/bayonet.png")).convert_alpha(), (50, 50))

special = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/up.png")).convert_alpha(),
                                 (50, 50))

scope = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "infantry/images/scope.png"))
                               .convert_alpha(), (50, 50))
rifle = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "infantry/images/rifle.png"))
                               .convert_alpha(), (50, 50))
money_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/money.png")).convert_alpha(), (50, 50))
clock_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/clock.png")).convert_alpha(), (50, 50))
s = sched.scheduler(time.time, time.sleep)


def get_line_col(x, y):
    line = y // BLOCKSIZE
    row = x // BLOCKSIZE
    return int(line), int(row)


class Game:
    def __init__(self, win):
        # VARS about screen :
        self.screen = win
        self.width = HEIGTH
        self.height = WIDTH
        # Background
        self.bg = pygame.image.load(os.path.join("game_assets", "misc/images/bg.jpeg"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        # Dimensions of the matrix :
        self.lines = LIGNES
        self.rows = COLONNES
        self.MAT = [[0 for _ in range(self.rows)] for _ in range(self.lines)]
        # Global values of the player :

        # List of enemies and units on the battle field :
        self.enemies = []
        self.allies = []
        # Main menu buttons :

        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_canon, "buy_canon", price_canon)
        self.menu.add_btn(buy_conscript, "buy_conscript", price_conscript)

        self.moving_object = None
        self.money = 150
        self.round = bool
        self.pause = True
        self.unit_menu = None
        self.selected_units = unit

        self.lines_font = pygame.font.SysFont("comicsans", 65)
        self.wave = 0
        self.phase = 0
        pygame.display.set_caption('Napoleon Defense')

        self.time = 0

        self.clock = pygame.time.Clock()

        self.selected_unit_to_buy = None
        self.selected_unit = None

        self.x = 0
        self.y = 0

    def run(self):
        music = pygame.mixer.Sound(os.path.join("game_assets", "misc/sounds/music.mp3"))
        music.set_volume(0.5)
        pygame.mixer.Channel(0).play(music, loops=-1)

        generated = False
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            self.time = pygame.time.get_ticks()
            self.play_sounds()
            self.draw()
            pos = pygame.mouse.get_pos()

            if pygame.time.get_ticks() > 10000:
                if not generated:
                    self.gen_army()
                    generated = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
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

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # SELECT UNIT ON THE BOARD TO BUY
                    self.x, self.y = get_line_col(pygame.mouse.get_pos()[0],
                                                  pygame.mouse.get_pos()[1])[0], \
                                     get_line_col(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
                    self.selected_unit = self.detect_select_unit()

                    side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                    if side_menu_button:
                        cost = self.menu.get_item_cost(side_menu_button)
                        if self.money >= cost:
                            self.selected_unit_to_buy = side_menu_button
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    if self.unit_menu:
                        unit_button = self.unit_menu.get_clicked(pos[0], pos[1])
                        if self.selected_unit:
                            if unit_button:
                                if str(unit_button) == "Level Up":
                                    self.upgrade_unit(self.selected_unit)

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
            self.update_mat(unites)

            for element in unites:
                if element.health <= 0:
                    if element.ally:
                        self.allies.remove(element)
                        break
                    else:
                        self.enemies.remove(element)
                        break
                if element.ally:
                    element.move(self.MAT, self.enemies)
                else:
                    element.move(self.MAT, self.allies)
                if element.ally:
                    element.attack(self.enemies)
                else:
                    element.attack(self.allies)

        pygame.quit()

    def play_sounds(self):
        """
        Play sounds of allies units
        :return: None
        """
        if self.time >= 10000:
            self.time = 0
            for element in self.allies:
                element.play_sound()

    def draw(self):
        """
        Draw all elements on the screen
        :return: None
        """
        phase = False
        if self.selected_unit_to_buy:
            phase = True
        self.screen.blit(self.bg, (0, 0))
        self.drawGrid(phase)
        self.draw_hover()
        if self.selected_unit:
            self.unit_menu = VerticalMenu(self.width - side_img.get_width() + 70, 800, unit_menu_img)
            self.selected_unit.draw_selected_unit(self.screen)
            self.unit_menu.add_btn(bayonet, "bayonet")
            self.unit_menu.add_btn(scope, "scope")
            self.unit_menu.add_btn(special, "special")
            self.unit_menu.add_btn(rifle, "rifle")
            # DO ACTION WHEN SELECTED UNIT
        for en in self.enemies:
            en.draw(self.screen)
        for element in self.allies:
            element.draw(self.screen)
            if element.name == "canon":
                element.draw_canon_ball(self.screen)
        lines, rows = len(self.MAT), len(self.MAT[0])

        for row in range(rows):
            for line in range(lines):
                if self.MAT[line][row] != 0:
                    rect = pygame.Rect((row * BLOCKSIZE), (line * BLOCKSIZE), BLOCKSIZE, BLOCKSIZE)
                    pygame.draw.rect(self.screen, [0, 0, 255, 0], rect, 1)

        # draw unit_menu
        if self.unit_menu:
            self.unit_menu.draw(self.screen)

        # draw menu , money
        self.menu.draw(self.screen)
        text = self.lines_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(money_img, (50, 50))
        start_x = self.width - 50 - 10

        self.screen.blit(text, (start_x - text.get_width() - 10, 75))
        self.screen.blit(money, (start_x, 65))
        # draw clock
        timer = self.lines_font.render(str(round(pygame.time.get_ticks() / 1000, 1)), 1, (255, 0, 0))
        clock = pygame.transform.scale(clock_img, (50, 50))
        self.screen.blit(timer, (self.width - text.get_width(), 20))
        self.screen.blit(clock, (self.width - text.get_width() - 50, 20))

        pygame.display.update()

    def Add_unit(self, name, ally, line, col):
        element = None
        if ally:
            if col < 4:
                if self.MAT[line][col] == 0:
                    if name == "buy_conscript":
                        element = Conscript(line, col, ally)
                        self.allies.append(element)
                    if name == "buy_canon":
                        element = Canon(line, col, ally)
                        self.allies.append(element)
        if not ally:
            if line < LIGNES and col < COLONNES:
                if self.MAT[line][col] == 0:
                    if name == "buy_conscript":
                        element = Conscript(line, col, ally)
                        self.enemies.append(element)
                    if name == "buy_old_gard":
                        element = OldGard(line, col, ally)
                        self.enemies.append(element)
                    if name == "anglais":
                        element = Anglais(line, col, ally)
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
        self.MAT = [[0 for _ in range(self.rows)] for _ in range(self.lines)]
        for element in units:
            unit_line = element.x
            unit_col = element.y
            line, col = get_line_col(unit_line, unit_col)
            self.MAT[line][col] = element.slug

    def drawGrid(self, phase):
        blksize = BLOCKSIZE  # Set the size of the grid block
        for x in range(self.rows):
            for y in range(self.lines):
                rect = pygame.Rect(x * blksize, y * blksize,
                                   blksize, blksize)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
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
        l, c = get_line_col(pygame.mouse.get_pos()[0],
                            pygame.mouse.get_pos()[1])[0], \
               get_line_col(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
        if l < LIGNES and c < COLONNES:
            slug = self.MAT[l][c]
            unit_hovered = find_unit_with_slug(self.enemies + self.allies, slug)
            if unit_hovered:
                unit_hovered.draw_radius(self.screen)
                unit_hovered.draw_health_bar(self.screen)
                unit_hovered.draw_info(self.screen)
            if self.MAT[l][c] == 0:
                pygame.draw.circle(self.screen, (255, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                                   BLOCKSIZE / 2, 1)
                # self.rows licks.append(pos)

    def detect_select_unit(self):
        try:
            line, row = self.x, self.y
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
                unit_leveled_up = MedGuard(element.line, element.row, element.ally)
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
        self.Add_unit("buy_conscript", False, 0, 24)
        self.Add_unit("buy_conscript", False, 2, 24)
        self.Add_unit("buy_conscript", False, 4, 24)
        self.Add_unit("buy_conscript", False, 6, 24)
        self.Add_unit("buy_conscript", False, 8, 24)
        self.Add_unit("buy_conscript", False, 10, 24)
        self.Add_unit("buy_conscript", False, 12, 24)
        self.Add_unit("buy_conscript", False, 14, 24)


def find_unit_with_slug(units, slug):
    for element in units:
        if element.slug == slug:
            return element
        else:
            pass
    return None
