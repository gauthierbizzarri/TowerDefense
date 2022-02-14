import sys , pygame
import os
import random
import sched, time
from settings import *
from units import unit
from units.anglais import Anglais
from units.conscrit import Conscrit
from units.fusiliet_de_ligne import Infanterie_de_ligne
from units.grenadier import Grenadier
from units.viellegarde import VielleGarde
from units.canon import Canon
from menu.menu import VerticalMenu
pygame.font.init()
pygame.init()


side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","misc/imgs/board.jpeg")).convert_alpha(), (120, 500))
star_img = pygame.image.load(os.path.join("game_assets","misc/imgs/star.png")).convert_alpha()

buy_vieille_garde= pygame.transform.scale(pygame.image.load(os.path.join("game_assets","infanterie/imgs/viellegarde.png")).convert_alpha(), (75, 75))

buy_conscrit= pygame.transform.scale(pygame.image.load(os.path.join("game_assets","infanterie/imgs/conscrit.png")).convert_alpha(), (75, 75))
buy_canon = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","misc/imgs/canon.png")).convert_alpha(), (75, 75))
money_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","misc/imgs/money.png")).convert_alpha(), (50, 50))
clock_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","misc/imgs/clock.png")).convert_alpha(), (50, 50))
s = sched.scheduler(time.time, time.sleep)

class Game:
    def __init__(self,win):
        self.screen =win
        self.width = HEIGTH
        self.height = WIDTH
        self.l = LIGNES
        self.c = COLONNES
        self.ennemies = []
        self.units = []
        self.moving_object = None
        self.money = 5000
        self.round = bool
        self.pause = True
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_canon, "buy_canon", price_canon)
        self.menu.add_btn(buy_conscrit, "buy_conscrit", price_conscrit)
        self.selected_units = unit
        self.bg = pygame.image.load(os.path.join("game_assets","misc/imgs/bg.jpeg"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.clicks = []
        self.wave = 0
        self.phase = 0
        pygame.display.set_caption('Napoleon Defense')

        self.last = 0

        self.clock = pygame.time.Clock()
        self.MAT = self.matrice()

        self.selected_unit_to_buy = None
        self.selected_unit = None

        self.x= 0
        self.y = 0

    def run(self):
        music = pygame.mixer.Sound(os.path.join("game_assets", "misc/sounds/music.mp3"))
        music.set_volume(0.5)
        pygame.mixer.Channel(0).play(music,loops=-1)

        generated = False
        run = True
        clock = pygame.time.Clock()
        self.matrice()
        while run :
            clock.tick(FPS)
            self.last = pygame.time.get_ticks()
            self.play_sounds()
            self.matrice()
            pos = pygame.mouse.get_pos()
            if pygame.time.get_ticks() > 30000:
                if not generated:
                    self.gen_army()
                    print("generated")
                    generated = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                #deployement phase
                if pygame.time.get_ticks() <= 30000 :
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.selected_unit_to_buy:
                            self.get_ligne_col(pos[0],pos[1])
                            if event.button==1:
                                ally = True
                            else :
                                ally =False

                            if self.check_free(self.get_ligne_col(pos[0],pos[1])[0],self.get_ligne_col(pos[0],pos[1])[1]):
                                self.Add_unit(self.selected_unit_to_buy,ally,self.get_ligne_col(pos[0],pos[1])[0],self.get_ligne_col(pos[0],pos[1])[1])

                if event.type == pygame.MOUSEBUTTONUP:
                    #SELECT UNIT ON THE BOARD TO BUY
                    side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                    if side_menu_button:
                        cost = self.menu.get_item_cost(side_menu_button)
                        if self.money >= cost:
                            self.selected_unit_to_buy = side_menu_button
                    #SELECT UNIT TO SHOW INFO
                    self.x, self.y = self.get_ligne_col(pygame.mouse.get_pos()[0],
                                  pygame.mouse.get_pos()[1])[0], \
                                        self.get_ligne_col(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]

                if event.type == pygame.KEYDOWN:
                    if self.selected_unit:
                        #BAYONET MODE
                        if event.key == pygame.K_b:
                            if self.selected_unit.cac == False :
                                self.selected_unit.cac = True
                            else:
                                self.selected_unit.cac = False
                        #LEVEL UP
                        if event.key == pygame.K_l:
                            self.upgrade_unit(self.selected_unit)


            #MOVING ALL UNITS IN THe BATTLE FIELD
            unites = []
            for k in range(len(self.ennemies)+len(self.units)):
                if k< len(self.ennemies):
                    unites.append(self.ennemies[k])
                if k < len(self.units):
                    unites.append(self.units[k])
            for unit in unites :

                if unit.health <= 0:
                    if unit.ally :
                        self.units.remove(unit)
                    else :
                        self.ennemies.remove(unit)
                        break
                unit.move(self.MAT)
                self.update_mat(unit)
                if unit.ally:
                    unit.attack(self.ennemies)
                else :
                    unit.attack(self.units)

            self.draw()

        pygame.quit()
    def play_sounds(self):
        if self.last >= 10000:
            self.last = 0
            for unit in self.units:
                unit.play_sound()

    def draw(self):
        phase = False
        if self.selected_unit_to_buy: phase = True
        self.screen.blit(self.bg,(0,0))
        self.drawGrid(phase)
        self.draw_hover()
        self.selected_unit=self.detect_select_unit()
        if self.selected_unit:
            self.selected_unit.draw_selected_unit(self.screen)
            #DO ACTION WHEN SELECTED UNIT
        for en in self.ennemies:
             en.draw(self.screen)
        for unit in self.units:
            unit.draw(self.screen)
        lignes , cols = len(self.MAT),len(self.MAT[0])

        for c in range(cols):
            for l in range(lignes):
                if self.MAT[l][c] !=0:
                    rect = pygame.Rect((c * BLOCKSIZE), (l * BLOCKSIZE), BLOCKSIZE, BLOCKSIZE )
                    pygame.draw.rect(self.screen, [0, 0, 255,0],rect, 1)

        self.menu.draw(self.screen)
        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(money_img, (50, 50))
        start_x = self.width - 50 - 10

        self.screen.blit(text, (start_x - text.get_width() - 10, 75))
        self.screen.blit(money, (start_x, 65))

        timer =  self.life_font.render(str(round(pygame.time.get_ticks()/1000,1)), 1, (255, 0, 0))
        if pygame.time.get_ticks()>30000:
            timer = self.life_font.render(str(pygame.time.get_ticks() / 1000), 1, (255, 255, 255))
        clock = pygame.transform.scale(clock_img, (50, 50))
        self.screen.blit(timer, (self.width- text.get_width() , 20))
        self.screen.blit(clock, (self.width -text.get_width()-50, 20))

        pygame.display.update()


    def Add_unit(self,name,ally,ligne,col):
        print(name,ally,ligne,col)
        object = None
        if ally :
            if col <4:
                if self.MAT[ligne][col] == 0:
                    if name =="buy_conscrit":
                        object = Conscrit(ligne, col, ally)
                        self.units.append(object)
                    if name =="buy_vieille_garde":
                        object = VielleGarde(ligne, col, ally)
                        self.units.append(object)
                    if name =="buy_canon":
                        object = Canon(ligne, col, ally)
                        self.units.append(object)
        if not ally :
            print(len(self.MAT),len(self.MAT[0]))
            if ligne <COLONNES and col<LIGNES:
                if self.MAT[ligne][col] == 0:
                    if name == "buy_conscrit":
                        object = Conscrit(ligne, col, ally)
                        self.ennemies.append(object)
                    if name == "buy_vieille_garde":
                        object = VielleGarde(ligne, col, ally)
                        self.ennemies.append(object)
                    if name =="anglais":
                        object = Anglais(ligne, col, ally)
                        self.ennemies.append(object)
        if object :
            self.money -= object.price
            self.update_mat(object)
            self.selected_unit_to_buy = None

    def matrice(self):
        Mat =[[0 for col in range(self.c)] for row in range(self.l)]
        self.MAT = Mat
    def check_free(self,x,y):
        try:
            if self.MAT[x][y] ==0:
                return True
            return False
        except:
            return False
    def update_mat(self,unit):
        unit_ligne = unit.x
        unit_col = unit.y
        ligne, col = self.get_ligne_col(unit_ligne,unit_col)
        self.MAT[ligne][col]=unit.name

    def get_ligne_col(self,x,y):
        ligne = y//BLOCKSIZE
        col = x // BLOCKSIZE
        return int(ligne),int(col)


    def drawGrid(self,phase):
        blockSize = BLOCKSIZE  # Set the size of the grid block
        for x in range(self.c):
            for y in range(self.l):
                rect = pygame.Rect(x * blockSize, y * blockSize,
                                   blockSize, blockSize)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
        if phase:
            for x in range(self.c):
                for y in range(self.l):

                    rect = pygame.Rect(x * blockSize, y * blockSize,
                                       blockSize, blockSize)
                    if x < 4:
                        pygame.draw.rect(self.screen, (0, 200, 0), rect, 2)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
    def draw_hover(self):
        l, c = self.get_ligne_col(pygame.mouse.get_pos()[0],
                                  pygame.mouse.get_pos()[1])[0], \
               self.get_ligne_col(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
        if l< LIGNES and c<COLONNES:
            slug  = self.MAT[l][c]
            unit_hovered = find_unit_with_slug(self.ennemies+self.units,slug)
            if unit_hovered:
                unit_hovered.draw_radius(self.screen)
                unit_hovered.draw_health_bar(self.screen)
                unit_hovered.draw_info(self.screen)
            if self.MAT[l][c] == 0:
                pygame.draw.circle(self.screen, (255, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), BLOCKSIZE/2, 1)
                # self.clicks.append(pos)
    def detect_select_unit(self):
        try :
            l,c = self.x , self.y
            if l <= LIGNES and c <= COLONNES:
                slug = self.MAT[l][c]
                unit_selected = find_unit_with_slug(self.ennemies + self.units, slug)
                if unit_selected:
                    return unit_selected
            return None
        except:
            pass

    def upgrade_unit(self,unit):
        #Upgrade conscrit
        if unit.level == 0:
            unit_leveled_up = Infanterie_de_ligne(unit.ligne, unit.colonne, unit.ally)
            self.units.append(unit_leveled_up)
            self.units.remove(unit)
        if unit.level == 1:
            unit_leveled_up = Grenadier(unit.ligne, unit.colonne, unit.ally)
            self.units.append(unit_leveled_up)
            self.units.remove(unit)
            return
        if unit.level == 2:
            unit_leveled_up = VielleGarde(unit.ligne, unit.colonne, unit.ally)
            self.units.append(unit_leveled_up)
            self.units.remove(unit)
            return

    def gen_army(self):
        for x in range (self.c):
                self.Add_unit("anglais",False,x,x)

def find_unit_with_slug(units,slug):
    for unit in units :
        if unit.name == slug :
            return unit
        else:
            pass
    return False
if __name__=='__main__':
    game = Game()
    game.run()