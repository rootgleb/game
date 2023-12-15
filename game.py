import pygame
import button
import config
from config import *
from random import *

pygame.init()
ARIAL_50 = pygame.font.SysFont("roboto", 50)
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Уровни")
clock = pygame.time.Clock()
current_scene = None


class Kvadrat:
    yellow = []
    red = []
    black = []
    blue = []
    tnt = []

    def clear(self, x, y):
        player = [x, y]
        if player in self.black:
            self.black.remove(player)
        if player in self.red:
            self.red.remove(player)
        if player in self.yellow:
            self.yellow.remove(player)

    def draw(self, s):
        if len(self.blue) != 0:
            for i in self.blue:
                pygame.draw.rect(s, BLUE, (int(i[0]), int(i[1]), 40, 40))
        if len(self.yellow) != 0:
            for i in self.yellow:
                pygame.draw.rect(s, YELLOW, (int(i[0]), int(i[1]), 40, 40))
        if len(self.red) != 0:
            for i in self.red:
                pygame.draw.rect(s, RED, (i[0], i[1], 40, 40))
        if len(self.black) != 0:
            for i in self.black:
                pygame.draw.rect(s, BLACK, (i[0], i[1], 40, 40))
        if len(self.tnt) != 0:
            for i in self.tnt:
                pygame.draw.rect(s, FIOLET, (i[0], i[1], 40, 40))


    def generate(self, level):
        di = pygame.display.get_window_size()
        count = level
        i = 0


        while i != count:
            tmp = [randrange(0, di[0], 40), randrange(0, di[1], 40)]


            if tmp not in self.yellow:
                if randrange(1, 100) == 1:
                    self.blue.append(tmp)
                elif randrange(1, 100) == 1:
                    self.tnt.append(tmp)
                else:
                    self.yellow.append(tmp)
            elif tmp not in self.red:
                self.red.append(tmp)
            elif tmp not in self.black:
                self.black.append(tmp)
                if randint(1, 2) == 1 and self.black != []:
                    c = choice(self.black)
                    self.black.remove(c)
                    self.red.remove(c)
                    self.yellow.remove(c)
            else:
                count += 1
            i += 1
            if i >= 30:
                break


def result(lvl, resultat):
    f = open("result", "r")
    tmp = [line[0: -1] for line in f]
    best = max(resultat, float(tmp[lvl - 1]))
    tmp[lvl - 1] = str(best)
    f.close()
    f = open("result", "w")
    f.write("\n".join(tmp) + "\n")
    f.close()
    return best


def switch_scene(scene):
    global current_scene
    current_scene = scene


def choose_level():
    di = pygame.display.get_window_size()
    img_easy = pygame.image.load("img/кнопка_уровень_легкий.png").convert_alpha()
    img_normal = pygame.image.load("img/кнопка_уровень_средний.png").convert_alpha()
    img_hard = pygame.image.load("img/кнопка_уровень_сложный.png").convert_alpha()
    img_close_button = pygame.image.load("img/зеленый_крестик.png").convert_alpha()
    btn_easy = button.Button(200, 200, img_easy, 0.5)
    btn_normal = button.Button(200, 400, img_normal, 0.5)
    btn_hard = button.Button(200, 600, img_hard, 0.5)
    btn_close = button.Button(di[0] - 50, 10, img_close_button, 0.05)
    pygame.font.init()
    text = ARIAL_50.render("Выберите уровень:", True, BLACK)
    running = True
    screen.fill(config.WHITE)
    screen.blit(text, (100, 100))
    while running:
        if btn_easy.draw(screen):
            running = False
            game(1)

        if btn_normal.draw(screen):
            running = False
            game(2)

        if btn_hard.draw(screen):
            running = False
            game(3)

        if btn_close.draw(screen):
            exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        clock.tick(FPS)
        pygame.display.flip()

###################################################


def game(level):
    running = True
    time = float(0)
    player = [40, 40]
    health = 100
    tnt = 0
    max_health = 100
    d = pygame.display.get_window_size()
    while running:
        screen.fill(config.WHITE)
        k = Kvadrat()
        k.generate(level)
        k.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a] and player[0] >= 40:
                    player[0] += -40
                elif event.key in [pygame.K_RIGHT, pygame.K_d] \
                        and player[0] + 60 <= pygame.display.get_window_size()[0]:
                    player[0] += 40
                elif event.key in [pygame.K_UP, pygame.K_w] and player[1] >= 40:
                    player[1] += -40
                elif event.key in [pygame.K_DOWN, pygame.K_s] \
                        and player[1] + 70 <= pygame.display.get_window_size()[1]:
                    player[1] += 40
                elif event.key == pygame.K_SPACE and tnt > 0:
                    tnt -= 1
                    for i in range(player[0] - 40, player[0] + 80, 40):
                        for j in range(player[1] - 40, player[1] + 80, 40):
                            k.clear(i, j)

        pygame.draw.line(screen, FIOLET, [0, 0], [round((d[0]/max_health)*health), 0], 20)
        pygame.draw.rect(screen, GREEN, (player[0], player[1], 40, 40))
        for i in range(0, d[1], 40):
            pygame.draw.line(screen, BLACK, [0, i], [d[0], i], 3)
        for i in range(0, d[0], 40):
            pygame.draw.line(screen, BLACK, [i, 0], [i, d[1]], 3)
        pygame.draw.line(screen, FIOLET, [0, 0], [round((d[0] / max_health) * health), 0], 20)
        pygame.font.init()
        text = ARIAL_50.render(f"Время: {round(time, 1)}", True, WHITE, BLACK)
        text2 = ARIAL_50.render(f"HP: {health}", True, WHITE, BLACK)
        text3 = ARIAL_50.render(f"TNT: {tnt}", True, WHITE, BLACK)
        time += 1 / FPS
        screen.blit(text, (10, d[1] - 50))
        screen.blit(text2, (10, d[1] - 100))
        screen.blit(text3, (10, d[1] - 150))
        if player in k.blue:
            health += 50
            if health > 100:
                health = 100
            k.blue.remove(player)
        if player in k.tnt:
            tnt += 1
            k.tnt.remove(player)
        if player in k.black:
            health -= 1
        if health == 0:
            Kvadrat.black = []
            Kvadrat.red = []
            Kvadrat.yellow = []
            Kvadrat.tnt = []
            Kvadrat.blue = []
            tnt = 0
            running = False
            game_over(level, time)
        clock.tick(FPS)
        pygame.display.flip()


def game_over(lvl, time):
    d = pygame.display.get_window_size()
    running = True
    screen.fill(config.WHITE)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        pygame.font.init()

        text = ARIAL_50.render(f"Ваш результат: {round(time, 2)}сек", True, BLACK)
        text1 = ARIAL_50.render(f"Лучший результат: {result(lvl, round(time, 2))}сек", True, BLACK)
        screen.blit(text, (d[0] // 2 - 250, 30))
        screen.blit(text1, (d[0] // 2 - 250, 150))

        img_play_again = pygame.image.load("img/играть_снова.png").convert_alpha()
        img_another_lvl = pygame.image.load("img/другой_уровень.png").convert_alpha()
        img_exit = pygame.image.load("img/выход.png").convert_alpha()
        btn_play_again = button.Button(200, 250, img_play_again, 0.35)
        btn_another_lvl = button.Button(200, 450, img_another_lvl, 0.35)
        btn_exit = button.Button(200, 650, img_exit, 0.35)

        if btn_another_lvl.draw(screen):
            running = False
            choose_level()
        if btn_play_again.draw(screen):
            running = False
            game(lvl)
        if btn_exit.draw(screen):
            exit(0)
        clock.tick(15)
        pygame.display.flip()


def run_ch_lvl():
    switch_scene(choose_level())
