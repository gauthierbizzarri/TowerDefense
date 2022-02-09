import pygame
import math
import os
def get_path(ligne,colonne):
    lignes = 11
    colonnes = 15
    all_path = []
    for c in range(colonnes):
        new_path = []
        for l in range(lignes):
                new_path.append((l*60,c*60))
        all_path.append(new_path)
    return all_path[ligne][colonne:]


class Unit :
    def __init__(self,ligne,colone,ally,width=64,height=64,velocity=3,):
        self.ligne = ligne
        self.colonne = colone
        self.ally = ally
        if self.ally:
            self.path = get_path(ligne,colone)
        else:
            self.path =  get_path(ligne,colone)[::-1]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.move_count = 0
        self.dis = 0

        self.level=1
        self.tower_imgs = []

        self.img = []
        self.animation_count = 0
        self.width = width
        self.height = height
        self.velocity = velocity
        self.range = 0
        self.max_health = 10
        self.health = 10
        self.flipped = False
        self.ammo = [1,2,3,4,5]
        self.accuracy = [1,2,3,4,5]
        self.reload_time = [1,2,3,4,5]
        self.upgrade_cost = [1,2,3,4,5]
        self.sell_price = [1,2,3,4,5]
        self.selected = False
        self.menu = ""
        self.ennemies = []
    def definepath(self):
        path = self.path

    def draw(self,surface):
        """
        draw the unit with the given images
        :param surface: surface
        :return: None
        """
        #self.animation_count += 1
        if self.animation_count >= len(self.imgs): self.animation_count = 0
        self.img = self.imgs[self.animation_count]

        surface.blit(self.img,(self.x,self.y))
        self.draw_health_bar(surface)
        if self.shooting:
            img = pygame.image.load(os.path.join("game_assets", "smoke.png"))
            img = pygame.transform.scale(img, (40, 40))
            surface.blit(img, (self.x, self.y))

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        if self.ally:
            pygame.draw.circle(win, (0, 255, 0),  (self.x  ,self.y - 7), 5, 0)
        else:
            pygame.draw.circle(win, (255, 0, 0),  (self.x  ,self.y - 7), 5, 0)
        pygame.draw.rect(win, (255, 0, 0), (self.x , self.y - 30, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x , self.y - 30, health_bar, 10), 0)
    def collide(self,x,y):
        """
        return if position has hit
        :param x:
        :param y:
        :return: bool
        """
        if x<self.x + self.width and x<self.x:
            if y<= self.y + self.height and y>= self.y :
                return True
        return False
    def click(self,X,Y):
        """
                returns if unit has been clicked on
                and selects unit if it was clicked
                :param X: int
                :param Y: int
                :return: bool
                """
        img = self.imgs[self.level - 1]
        if X <= self.x - img.get_width() // 2 + self.width and X >= self.x - img.get_width() // 2:
            if Y <= self.y + self.height - img.get_height() // 2 and Y >= self.y - img.get_height() // 2:
                return True
            print("clicked")
        return False
    def sell(self):
        return self.sell_price
    def upgrade(self):
        if self.level < len(self.tower_imgs):
            self.level += 1
            self.damage += 1
    def get_upgrade_cost(self):
        return self.upgrade_cost[self.level -1]
    def move(self):
        """
        Move enemy
        :return: None
        """

        if not self.shooting :
            self.animation_count += 1
            if self.animation_count >= len(self.imgs):
                self.animation_count = 0

            x1, y1 = self.path[self.path_pos]
            if self.path_pos + 1 >= len(self.path):
                x2, y2 = (-10, 355)
            else:
                x2, y2 = self.path[self.path_pos+1]

            dirn = ((x2-x1), (y2-y1))
            length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
            dirn = (dirn[0]/length, dirn[1]/length)
            if dirn[0] < 0 and not (self.flipped):
                self.flipped = True
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)

            move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

            self.x = move_x
            self.y = move_y

            # Go to next point
            if dirn[0] >= 0: # moving right
                if dirn[1] >= 0: # moving down
                    if self.x >= x2 and self.y >= y2:
                        self.path_pos += 1
                else:
                    if self.x >= x2 and self.y <= y2:
                        self.path_pos += 1
            else: # moving left
                if dirn[1] >= 0:  # moving down
                    if self.x <= x2 and self.y >= y2:
                        self.path_pos += 1
                else:
                    if self.x <= x2 and self.y >= y2:
                        self.path_pos += 1

    def hit(self,dommages):
        """
        returns if unit has died
        :return:
        """
        self.health -= dommages
        if self.health <= 0: return True
        return False

