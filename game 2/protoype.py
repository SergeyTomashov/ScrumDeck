# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math
import functions
from functions import load_image

ch = 0
pygame.init()
SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1028
screen = pygame.display.set_mode(SIZE_SCREEN)


def terminate():
    pygame.quit()
    sys.exit()


def lines(all_elements, connections, screen, flag):
    if connections:
        for i in all_elements:
            if i.index in connections:
                if i.char == "or":
                    x1 = i.rect.x + 174
                    y1 = i.rect.y
                if i.char == "inverse":
                    x1 = i.rect.x + 182
                    y1 = i.rect.y
                if i.char == "cleat":
                    x1 = i.rect.x
                    y1 = i.rect.y - 43
                index2 = connections[i.index]
                if index2 == None:
                    break
                for j in all_elements:
                    if j.index == index2:
                        if j.char == "inverse":
                            x2 = j.rect.x
                            y2 = j.rect.y + 24
                        else:
                            x2 = j.rect.x
                            y2 = j.rect.y

                        if not j.input_1 or j.input_1 == i.index:
                            pygame.draw.line(screen, (0, 0, 0), (x1, y1 + 44), ((x2 - x1) // 2 + x1, y1 + 44))
                            pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y1 + 44), ((x2 - x1) // 2 + x1, y2 + 22))
                            pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y2 + 22), (x2, y2 + 22))
                            j.input_1 = i.index
                        else:
                            pygame.draw.line(screen, (0, 0, 0), (x1, y1 + 44), ((x2 - x1) // 2 + x1, y1 + 44))
                            pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y1 + 44), ((x2 - x1) // 2 + x1, y2 + 66))
                            pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y2 + 66), (x2, y2 + 66))
    if flag:
        n = sortic(all_el)
        t = n[5]
        while t.index in connections:
            t = n[connections[t.index]]

        if t.char == "or":
            x1 = t.rect.x + 174
            y1 = t.rect.y
        if t.char == "inverse":
            x1 = t.rect.x + 182
            y1 = t.rect.y
        x2 = 1852
        y2 = 654
        pygame.draw.line(screen, (0, 0, 0), (x1, y1 + 44), ((x2 - x1) // 2 + x1, y1 + 44))
        pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y1 + 44), ((x2 - x1) // 2 + x1, y2))
        pygame.draw.line(screen, (0, 0, 0), ((x2 - x1) // 2 + x1, y2), (x2, y2))



def sortic(all_elements):
    n = {}
    for i in all_elements:
        n[i.index] = i
    return n



def determinant(connections, all_elements):
    for i in all_elements:
        if i.index == 4:
            a = i.condition
        if i.index == 5:
            b = i.condition
    n = sortic(all_elements)
    t = n[connections[4]]
    while t.char != "or":
        if t.char == "inverse":
            a = not a
        t = n[connections[t.index]]
    t = n[connections[5]]
    while t.char != "or":
        if t.char == "inverse":
            b = not b
        t = n[connections[t.index]]
    c = a or b
    if t.index in connections:
        c = not c
    return c


class feature_or(pygame.sprite.Sprite):
    image1 = load_image("or3.png")
    image2 = load_image("inverse.png")
    image3 = load_image("cleat.png")
    image4 = load_image("cleat_2.png")

    def __init__(self, feature_or_sprite, index, x, y, char):
        super().__init__(feature_or_sprite)
        if char == "or":
            self.image = feature_or.image1
        if char == "inverse":
            self.image = feature_or.image2
        if char == "cleat":
            self.image = feature_or.image3
            self.condition = False
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.index = index
        self.char = char
        self.input_1 = False
        self.input_2 = False



class Lamp_sprite(pygame.sprite.Sprite):
    image1 = load_image("lamp.png", convert=(105, 154))
    image2 = load_image("lamp_2.png", convert=(105, 154))

    def __init__(self, feature_or_sprite):
        super().__init__(feature_or_sprite)
        self.image = Lamp_sprite.image1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.condition = False
        self.rect.x = 1800
        self.rect.y = 500




fon = pygame.transform.scale(load_image('background.png'), (1920, 1080))
main_running = True
draging = False
current_coor = None
all_el = []
connections = {}
lines_list = []
status = "moving"
first_choose_index, el_coor, moving_index = None, None, None
_or_ = pygame.sprite.Group()
first = feature_or(_or_, 1, 20, 20, "inverse")
second = feature_or(_or_, 2, 300, 20, "or")
third = feature_or(_or_, 3, 600, 20, "inverse")
fourth = feature_or(_or_, 6, 900, 20, "inverse")
cleat_1, cleat_2  = feature_or(_or_, 5, 0, 405, "cleat"), feature_or(_or_, 4, 0, 675, "cleat")
all_el = [first, second, third, fourth, cleat_1, cleat_2]
lamp = pygame.sprite.Group()
Lamp = Lamp_sprite(lamp)
flag = False
while main_running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_running = False
        if pygame.key.get_pressed()[pygame.K_a]:
            status = "moving"
        if pygame.key.get_pressed()[pygame.K_s]:
            status = "connecting"
        if pygame.key.get_pressed()[pygame.K_d]:
            Lamp.image = Lamp_sprite.image1
            connections = {}
            first_choose_index = False
            flag = False
        if pygame.key.get_pressed()[pygame.K_w]:
            flag = True
            if determinant(connections, all_el):
                Lamp.image = Lamp_sprite.image2
            else:
                Lamp.image = Lamp_sprite.image1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if cleat_1.condition:
                    cleat_1.condition = False
                    cleat_1.image = feature_or.image3
                else:
                    cleat_1.condition = True
                    cleat_1.image = feature_or.image4
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                if cleat_2.condition:
                    cleat_2.condition = False
                    cleat_2.image = feature_or.image3
                else:
                    cleat_2.condition = True
                    cleat_2.image = feature_or.image4



        if event.type == pygame.MOUSEBUTTONDOWN:
            el_coor = pygame.mouse.get_pos()
            if status == "moving":
                draging = True
                for i in all_el[:4]:
                    i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                    if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                        if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                            moving_index = i.index
            elif status == "connecting" and not first_choose_index:
                for i in all_el:
                    i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                    if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                        if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                            first_choose_index = i.index
                if el_coor[0] > 30 and el_coor[0] < 230 and el_coor[1] > 458 and el_coor[1] < 558:
                    first_choose_index = 5
                elif el_coor[0] > 30 and el_coor[0] < 230 and el_coor[1] > 730 and el_coor[1] < 830:
                    first_choose_index = 4

            elif status == "connecting" and first_choose_index:
                for i in all_el[:4]:
                    i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                    if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                        if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                            second_choose_index = i.index
                            if first_choose_index in connections:
                                if connections[first_choose_index] != second_choose_index:
                                    connections[first_choose_index] = second_choose_index
                                else:
                                    connections[first_choose_index] = None
                            else:
                                connections[first_choose_index] = second_choose_index
                            first_choose_index = None

        if draging:
            if event.type == pygame.MOUSEMOTION:
                current_coor = pygame.mouse.get_pos()
                for i in all_el:
                    if i.index == moving_index:
                        i.rect.x += current_coor[0] - el_coor[0]
                        i.rect.y += current_coor[1] - el_coor[1]
                el_coor = current_coor


        if event.type == pygame.MOUSEBUTTONUP:
            draging = False
            moving_index = None



    screen.blit(fon, (0, 0))
    lines(all_el, connections, screen, flag)
    _or_.draw(screen)
    lamp.draw(screen)
    _or_.update()
    pygame.display.flip()


pygame.quit()