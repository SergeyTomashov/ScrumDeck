# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math
import functions
from functions import load_image
pygame.init()
SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1028
screen = pygame.display.set_mode(SIZE_SCREEN)





def start():
    ch = 0
    pygame.init()
    SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1028
    screen = pygame.display.set_mode(SIZE_SCREEN)

    fon = pygame.transform.scale(load_image('background.png'), (1920, 1080))
    first_choose_index = None
    moving_index = None
    draging = False
    status = "moving"
    connections = {}
    all_el = []
    main_list = []
    t = pygame.time.get_ticks()
    t_2 = pygame.time.get_ticks()

    feature = pygame.sprite.Group()
    first = features(feature, 0, 20, 20, "inverse")
    second = features(feature, 1, 300, 20, "or")
    third = features(feature, 2, 600, 20, "inverse")
    fourth = features(feature, 3, 900, 20, "inverse")
    trigger_1 = features(feature, 4, 0, 405, "trigger")
    trigger_2 = features(feature, 5, 0, 675, "trigger")
    lamp_1 = features(feature, 6, 1625, 50, "lamp")
    lamp_2 = features(feature, 7, 1625, 250, "lamp")
    lamp_3 = features(feature, 8, 1625, 450, "lamp")
    lamp_4 = features(feature, 9, 1625, 650, "lamp")
    all_el = [first, second, third, fourth, trigger_1, trigger_2, lamp_1, lamp_2, lamp_3, lamp_4]

    main_running = True
    while main_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                main_running = False
            if pygame.key.get_pressed()[pygame.K_a]:
                status = "moving"
            if pygame.key.get_pressed()[pygame.K_1]:
                if (pygame.time.get_ticks() - t) // 1000 > 1:
                    if trigger_1.status == [0]:
                        trigger_1.image = features.image3
                        trigger_1.status = [1]
                    else:
                        trigger_1.image = features.image6
                        trigger_1.status = [0]
                    t = pygame.time.get_ticks()
            if pygame.key.get_pressed()[pygame.K_2]:
                if (pygame.time.get_ticks() - t_2) // 1000 > 1:
                    if trigger_2.status == [0]:
                        trigger_2.image = features.image3
                        trigger_2.status = [1]
                    else:
                        trigger_2.image = features.image6
                        trigger_2.status = [0]
                    t_2 = pygame.time.get_ticks()
            if pygame.key.get_pressed()[pygame.K_s]:
                status = "connecting"
            if pygame.key.get_pressed()[pygame.K_d]:
                connections = {}
                first_choose_index = None
            if pygame.key.get_pressed()[pygame.K_w]:
                algoritm(connections, all_el)

            if event.type == pygame.MOUSEBUTTONDOWN:
                el_coor = pygame.mouse.get_pos()
                if status == "moving":
                    draging = True
                    for i in all_el:
                        i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                        if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                            if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                                if i.char != "lamp" and i.char != "trigger":
                                    moving_index = i.index

                elif status == "connecting" and first_choose_index == None:
                    for i in all_el:
                        i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                        if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                            if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                                if i.char != "lamp":
                                    first_choose_index = i.index

                elif status == "connecting":
                    for i in all_el:
                        i.coords = [[i.rect.x, i.rect.x + 179], [i.rect.y, i.rect.y + 91]]
                        if el_coor[0] > i.coords[0][0] and el_coor[0] < i.coords[0][1]:
                            if el_coor[1] > i.coords[1][0] and el_coor[1] < i.coords[1][1]:
                                if i.char != "trigger":
                                    second_choose_index = i.index
                                    if first_choose_index in connections:
                                            connections[first_choose_index].append(second_choose_index)
                                    else:
                                        connections[first_choose_index] = [second_choose_index]
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
        Sortic(connections, all_el, screen)
        feature.draw(screen)
        feature.update()
        pygame.display.flip()


    pygame.quit()



def terminate():
    pygame.quit()
    sys.exit()


class features(pygame.sprite.Sprite):
    image1 = load_image("or3.png")
    image2 = load_image("inverse.png")
    image3 = load_image("trigger_1.png")
    image6 = load_image("trigger_2.png")
    image4 = load_image("lamp_dis.png")
    image5 = load_image("lamp_en.png")

    def __init__(self, feature_sprite, index, x, y, char):
        super().__init__(feature_sprite)
        if char == "or":
            self.image = features.image1
            self.status = [None, None]
        if char == "inverse":
            self.image = features.image2
            self.status = [None]
        if char == "trigger":
            self.image = features.image3
            self.condition = False
            self.status = [1]
        if char == "lamp":
            self.image = features.image4
            self.status = [None]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.index = index
        self.char = char
        self.input = False
        self.count = 0






def Lines(x_1, y_1, x_2, y_2, char_1, char_2, obj, screen):
    if char_1 == "or":
        x_1 += 174
        y_1 += 44
    if char_1 == "inverse":
        x_1 += 182
        y_1 += 46
    if char_1 == "trigger":
        x_1 += 196
        y_1 += 41
    if char_2 == "or":
        if obj.input:
            y_2 += 23
            obj.input = False
        else:
            y_2 += 64
        x_2 += 0
    if char_2 == "inverse":
        x_2 += 2
        y_2 += 48
    if char_2 == "lamp":
        x_2 += -68
        y_2 += 146
    pygame.draw.line(screen, (0, 0, 0), (x_1, y_1), ((x_2 - x_1) // 2 + x_1, y_1))
    pygame.draw.line(screen, (0, 0, 0), ((x_2 - x_1) // 2 + x_1, y_1), ((x_2 - x_1) // 2 + x_1, y_2))
    pygame.draw.line(screen, (0, 0, 0), ((x_2 - x_1) // 2 + x_1, y_2), (x_2, y_2))


def Sortic(connections, all_el, screen):
    for i in all_el:
        i.input = True
    for i in connections:
        for j in connections[i]:
            if j != i:
                Lines(all_el[i].rect.x, all_el[i].rect.y,
                all_el[j].rect.x, all_el[j].rect.y,
                all_el[i].char, all_el[j].char, all_el[j], screen)


def algoritm(connections, all_el):
    k = []
    t = False
    while not t:
        for i in connections:
            if None not in all_el[i].status:
                for j in connections[i]:
                    if len(all_el[j].status) == 2:
                        if all_el[j].status[0] == None and [i, j] not in k:
                            all_el[j].status[0] = all_el[i].status[0]
                            k.append([i, j])
                        elif all_el[j].status[1] == None and [i, j] not in k:
                            all_el[j].status[1] = all_el[i].status[0]
                            k.append([i, j])
                            all_el[j].status = [all_el[j].status[0] or all_el[j].status[1]]
                    else:
                        if all_el[j].status[0] == None and [i, j] not in k:
                            if all_el[j].char == "inverse":
                                all_el[j].status[0] = not all_el[i].status[0]
                            else:
                                all_el[j].status[0] = all_el[i].status[0]
                            k.append([i, j])

        t = True
        for i in connections:
            for j in connections[i]:
                if all_el[j] == "lamp":
                    if all_el[j].status == None:
                        t = False

    for i in all_el:
        if i.char == "lamp":
            if i.status == [True]:
                i.image = features.image5
                i.status = [None]
            else:
                i.image = features.image4
                i.status = [None]
        if i.char == "inverse":
            i.status = [None]
        if i.char == "or":
            i.status = [None, None]



start()