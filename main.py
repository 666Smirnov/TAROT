import pygame
import random
import pygame_button
import pygame.image
import os, sys
from pygame.locals import *
import pygame as pg
from pygame.surface import Surface

import TARO
import test2

WIDTH  = 1920
HEIGHT =  1080
FPS    =   60

# Задаем цвета
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)

# переменные
GM_T = 1450
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tarot v0.1")
clock = pygame.time.Clock()
score = "ну чё погнали ?!"
font_name = pygame.font.match_font('arial')
size = screen.get_size()
width = size[0]
height = size[1]
game_state = "Menu1"
game_menu = False
pygame.mouse.set_visible(False)  # hide the cursor
cursor_img = pygame.image.load('coursor-1.png')
cursor_img1 = pygame.image.load('coursor-2.png')
cursor_img_rect = cursor_img.get_rect()

class text():
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        #self.width = width
        #self.height = height
        self.path = path
        self.text_p = ''

        with open(self.path, "r") as f:
            text1 = f.read()
            self.text_p += text1

    def blit_text(self,pov, pos, size, color=BLACK):
        font = pygame.font.SysFont('Arial', size)
        words = [word.split(' ') for word in self.text_p.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = pov.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                pov.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


def rasklad(type_game):
    ras = TARO.start()
    key = list(ras.keys())
    if type_game == 'Карта дня':
        return ras[str(key[0])]
class karta():
    def __init__(self,color, x, y, width, height, image):
        self.image = image
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

class button():
    def __init__(self, color, x, y, width, height, image_path=('btn.png','btn1.png','btn2.png'), text='',  type_btn=True):
        self.type_btn = type_btn
        self.image1 = pygame.image.load(image_path[0])
        self.image2 = pygame.image.load(image_path[1])
        self.image3 = pygame.image.load(image_path[2])
        self.image_rect = self.image1.get_rect()
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.radius = 33
    def draw(self, win, outline=None, type_btn=True):
        # Call this method to draw the button on the screen
        #if outline:
            #pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.type_btn:
            pos = pygame.mouse.get_pos()
            pygame.draw.rect(win, self.color, (self.x, self.y, self.image_rect[2], self.image_rect[3]), 0)
            win.blit(self.image1, (self.x, self.y))
            if self.isOver(pos):
                win.blit(self.image2, (self.x, self.y))
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1:  # левая кнопка мыши
                        win.blit(self.image3, (self.x, self.y))
            if game_menu:
                pos_r = (pos[0] - 1450, pos[1])
                if self.isOver(pos_r):
                    win.blit(self.image2, (self.x, self.y))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # левая кнопка мыши
                            win.blit(self.image3, (self.x, self.y))

        else:
            pygame.draw.circle(win,  self.color, (self.x + self.width/2, self.y + self.height/2), (self.radius))
            img = pygame.image.load('Menu_sandwich.png')
            img = pygame.transform.scale(img, (70, 70))
            win.blit(img, (self.x, self.y))
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            #win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
    def isOverGM(self, pos, GM_T):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > GM_T + 115 and pos[0] < GM_T + 115 + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

class Menu1():
    def __init__(self):

        self.btn_Tarot = button( (0, 255, 0), 460, 845, 395, 115,('tarot-1.png','tarot-2.png','tarot-3.png'), text="Таро")
        self.btn_NoTarot = button((255, 0, 0), 1065, 845, 395, 115, text="Не таро")
        self.bg = pygame.image.load("Menu1.jpg")
    def look(self):
        screen.blit(self.bg, (0, 0))
        self.btn_Tarot.draw(screen, (0, 0, 0))
        self.btn_NoTarot.draw(screen, (0, 0, 0))


class Menu2():
    def __init__(self):
        self.card1 = button((BLUE), 790, 300, 395, 100, text="Карта дня")
        self.card2 = button((BLUE), 790, 450, 395, 100, text="Три карты")
        self.card3 = button((BLUE), 790, 600, 395, 100, text="Кельтский крест")
        self.card4 = button((BLUE), 790, 750, 395, 100, text="Вокзал для двоих")
        self.bg = pygame.image.load("Menu2.png")
    def look(self):
        screen.fill((BLACK))
        screen.blit(self.bg, (0, 0))
        self.card1.draw(screen, (0, 0, 0))
        self.card2.draw(screen, (0, 0, 0))
        self.card3.draw(screen, (0, 0, 0))
        self.card4.draw(screen, (0, 0, 0))

class Menu1card:
    def __init__(self):
        self.bg = pygame.image.load("Menu1card.jpg")
        self.lbl = rasklad(type_game='Карта дня')
        self.image = pygame.image.load(self.lbl[0] + '.jpg')
        x = self.image.get_rect()
        self.card = karta(GREEN, 300, 300, x[2], x[3], self.image)


    def look(self):
        t = text(0, 0, self.lbl[1])
        w = Surface((500, 500))
        w.fill(WHITE)
        self.bg.blit(w,(0, 0))
        scrollbar = test2.ScrollBar(500, w)
        #self.bg.scroll(0, 1)                         #########
        t.blit_text(self.bg, (0, 0), 32)

        self.bg.blit(self.image, (300, 300))
        scrollbar.draw(w)

        screen.blit(self.bg, (0, 0))

class GameMenu():
    global game_menu
    def __init__(self):
        self.surf = pg.Surface((470, 1080))
        self.surf.fill((255, 255, 255))
        self.exit_btn = button(RED, 115, 600, 250, 70, text="Выход")
        self.Gbg = pygame.image.load("GameMenu.png")

    def open(self):
        self.exit_btn.draw(self.Gbg, (BLACK))
        #screen.blit(self.surf, (GM_T, 0))
        screen.blit(self.Gbg, (1450, 0))

    def close(self):
        pass
        #print('Close')

GM = GameMenu()
menu_1 = Menu1()
menu_2 = Menu2()
menu_1_card = Menu1card()
btn_menu = button(YELLOW, 1789, 67, 70, 70, text="Меню", type_btn=False)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if GM.exit_btn.isOverGM(pos, GM_T) and GM_open:
                print('Clicked Exit')
                running = False
                pygame.quit()
                quit()
            if menu_1.btn_Tarot.isOver(pos) and game_state == "Menu1":
                game_state = "Menu2"
            if menu_1.btn_NoTarot.isOver(pos) and game_state == "Menu1":
                pass
            if menu_2.card1.isOver(pos) and game_state == "Menu2":
                game_state = 'Menu1card'
            if btn_menu.isOver(pos):
                if not (game_menu):
                    game_menu = True
                else:
                    game_menu = False



        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if game_state == "Menu1":
            menu_1.look()

        elif game_state == 'Menu2':
            menu_2.look()
        elif game_state == 'Menu1card':
            menu_1_card.look()


    if game_menu:
        GM.open()
        GM_open = True
    else:
        GM.close()
        GM_open = False
    # Курсор
    btn_menu.draw(screen, (0, 0, 0))
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # левая кнопка мыши

            screen.blit(cursor_img1, cursor_img_rect.center)
    else:
        screen.blit(cursor_img, cursor_img_rect.center)

        # Обновление

    pygame.display.update()
    # Рендеринг
    #screen.fill(BLACK)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()