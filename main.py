# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math


ch = 0
pygame.init()
SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1028
screen = pygame.display.set_mode(SIZE_SCREEN)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None, convert=None):
    fullname = os.path.join("data", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if convert is not None:
        image = pygame.transform.scale(image, convert)
    return image





class feature_or(pygame.sprite.Sprite):
    image1 = load_image("or.png")

    def __init__(self, feature_or_sprite, index, x, y, char):
        super().__init__(feature_or_sprite)
        self.image = feature_or.image1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.coords = [[self.rect.x , self.rect.x + 192], [self.rect.y, self.rect.y + 108]]
        self.index = index
        self.char = char



    def update(self):
        pass









fon = pygame.transform.scale(load_image('background.png'), (1920, 1080))
main_running = True
draging = False
current_coor = None
all_el = []
connections = []
lines_list = []
while main_running:
    _or_ = pygame.sprite.Group()
    first = feature_or(_or_, 0, 20, 20, "or")
    second = feature_or(_or_, 1, 500, 500, "or")
    all_el.append(first)
    all_el.append(second)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_coor = pygame.mouse.get_pos()
            for i in all_el:
                if start_coor[0] > i.coords[0][0] and start_coor[0] < i.coords[0][1]:
                    if start_coor[1] > i.coords[1][0] and start_coor[1] < i.coords[1][1]:
                        draging = True
                        draging_from = i.index
        if event.type == pygame.MOUSEBUTTONUP:
            if draging:
                for i in all_el:
                    if current_coor[0] > i.coords[0][0] and current_coor[0] < i.coords[0][1]:
                        if current_coor[1] > i.coords[1][0] and current_coor[1] < i.coords[1][1]:
                            if draging_from != i.index:
                                connections.append([draging_from, i.index])
                                lines_list.append([[start_coor,(current_coor[0], start_coor[1])],
                                                   [(current_coor[0], start_coor[1]), (current_coor[0], current_coor[1])]])


            draging = False
            current_coor = None

        if draging:
            if event.type == pygame.MOUSEMOTION:
                current_coor = pygame.mouse.get_pos()
    screen.blit(fon, (0, 0))
    if draging and current_coor:
        pygame.draw.line(screen, (24, 24, 24), start_coor, (current_coor[0], start_coor[1]))
        pygame.draw.line(screen, (24, 24, 24), (current_coor[0], start_coor[1]), (current_coor[0], current_coor[1]))
    for i in lines_list:
        pygame.draw.line(screen, (24, 24, 24), i[0][0], i[0][1])
        pygame.draw.line(screen, (24, 24, 24), i[1][0], i[1][1])
    _or_.draw(screen)
    _or_.update()
    pygame.display.flip()


pygame.quit()
