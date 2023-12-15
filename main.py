import pygame
import button
import game
from config import *
from pygame import font

pygame.init()
ARIAL_50 = font.SysFont("roboto", 50)
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Игра")
clock = pygame.time.Clock()
btn_play_img = pygame.image.load("img/кнопка_играть.png").convert_alpha()
btn_quit_img = pygame.image.load("img/кнопка_выйти.png").convert_alpha()
btn_info_img = pygame.image.load("img/кнопка_инфо.png").convert_alpha()
btn_in_main_menu = pygame.image.load("img/кнопка_в_главное_меню.png").convert_alpha()
current_scene = None


def switch_scene(scene):
    global current_scene
    current_scene = scene


def menu():
    screen.fill(WHITE)
    running = True
    play_button = button.Button(500 - 5, 10, btn_play_img, 0.7)
    quit_button = button.Button(500, 410, btn_quit_img, 0.7)
    info_button = button.Button(510, 210, btn_info_img, 0.7)
    while running:
        screen.fill(WHITE)
        if play_button.draw(screen):
            running = False
            game.run_ch_lvl()

        if quit_button.draw(screen):
            running = False
            exit(0)

        if info_button.draw(screen):
            running = False
            info()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        clock.tick(FPS)
        pygame.display.flip()


def info():
    pygame.font.init()
    running = True
    exit_button = button.Button(200, 510, btn_in_main_menu, 0.5)
    while running:
        screen.fill(WHITE)
        if exit_button.draw(screen):
            running = False
            switch_scene(menu())

        text = ARIAL_50.render("Управление - стрелки и кнопки wasd", True, BLACK)
        text1 = ARIAL_50.render("Здесь нужно избегать черные клетки", True, BLACK)
        text2 = ARIAL_50.render("", True, BLACK)
        screen.blit(text, (50, 50))
        screen.blit(text1, (50, 100))
        screen.blit(text2, (50, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        clock.tick(FPS)
        pygame.display.flip()


switch_scene(menu())
