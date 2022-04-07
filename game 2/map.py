# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math
import functions
from functions import load_image
from main_function import *


ch = 0
pygame.init()
SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1028
screen = pygame.display.set_mode(SIZE_SCREEN)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
speed = 10
movement = None
clock = pygame.time.Clock()
fps = 15
fps_clock = pygame.time.Clock()



class Character(pygame.sprite.Sprite):
    im_front_1 = load_image("ch_f1.png", convert=(100, 150))
    im_front_2 = load_image("ch_f2.png", convert=(100, 150))
    im_front_3 = load_image("ch_f3.png", convert=(100, 150))
    im_left_1 = load_image("ch_l1.png", convert=(90, 150))
    im_left_2 = load_image("ch_l2.png", convert=(90, 155))
    im_left_3 = load_image("ch_l3.png", convert=(90, 155))
    im_right_1 = load_image("ch_r1.png", convert=(90, 150))
    im_right_2 = load_image("ch_r2.png", convert=(90, 155))
    im_right_3 = load_image("ch_r3.png", convert=(90, 155))
    im_behind_1 = load_image("ch_b1.png", convert=(100, 150))
    im_behind_2 = load_image("ch_b2.png", convert=(100, 150))
    im_behind_3 = load_image("ch_b3.png", convert=(100, 150))
    all_images = [
        [im_behind_1, im_behind_2, im_behind_3],
        [im_left_1, im_left_2, im_left_3],
        [im_front_1, im_front_2, im_front_3],
        [im_right_1, im_right_2, im_right_3]
    ]

    def __init__(self, character_sprite, speed):
        super().__init__(character_sprite)
        self.image = Character.im_front_1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.im_front_1)
        self.mask = pygame.mask.from_surface(self.image)
        self.all_images = {}
        self.direction = [speed, 0]
        self.all_images[f"[0, -{speed}]"] = Character.all_images[0]
        self.all_images[f"[-{speed}, 0]"] = Character.all_images[1]
        self.all_images[f"[0, {speed}]"] = Character.all_images[2]
        self.all_images[f"[{speed}, 0]"] = Character.all_images[3]
        self.speed = speed
        self.images = self.all_images[str(self.direction)]
        self.flag = True
        self.rect.x = 900
        self.rect.y = 500

    def moving(self, direction):
        if direction:
            if self.direction != direction:
                self.direction = direction
                self.images = self.all_images[str(direction)]
                self.flag = True

            # if not self.col:
            self.rect = self.rect.move(direction)

            if self.flag:
                self.image = self.images[1]
            else:
                self.image = self.images[2]
            self.flag = not self.flag
        else:
            self.image = self.images[0]



character_sprite = pygame.sprite.Group()
character = Character(character_sprite, speed)


fon = pygame.transform.scale(load_image('map.png'), (1920, 1080))
main_running = True
flag = False
speech = 0
a = open("F:/game/replics.txt", encoding='utf-8').readlines()
b = ["Марк", "Марк", "Марк", "Я", "Марк", "Марк", "Марк", "Марк"]
print(a)

while main_running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_running = False

        if pygame.key.get_pressed()[pygame.K_a]:
            movement = [-speed, 0]
        elif pygame.key.get_pressed()[pygame.K_s]:
            movement = [0, speed]
        elif pygame.key.get_pressed()[pygame.K_w]:
            movement = [0, -speed]
        elif pygame.key.get_pressed()[pygame.K_d]:
            movement = [speed, 0]
        else:
            movement = None
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            main_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            el_coor = pygame.mouse.get_pos()

        if pygame.key.get_pressed()[pygame.K_e]:
            if character.rect.x > 860 and character.rect.x < 1590:
                if character.rect.y > 420 and character.rect.y < 500:
                    start()
            if character.rect.x > 490 and character.rect.x < 680:
                if character.rect.y > 400 and character.rect.y < 470:
                    if not flag:
                        flag = True
                        t = pygame.time.get_ticks()
                    elif (pygame.time.get_ticks() - t) // 1000 > 1:
                        speech += 1
                        t = pygame.time.get_ticks()
                    if speech > len(a):
                        flag = False

    fps_clock.tick(fps)
    character.moving(movement)
    character.update()
    screen.blit(fon, (0, 0))
    character_sprite.draw(screen)
    if flag:
        pygame.draw.rect(screen, (255, 255, 255), [560, 550, 700, 240], 2)
        pygame.draw.line(screen, (255, 255, 255), [560, 580], [1260, 580], 2)
        font = pygame.font.SysFont("comicsans", 30)
        text_2 = a[speech]
        text_1 = b[speech]
        text1 = font.render(text_1, True, (255, 255, 255))
        text2 = font.render(text_2[:-1], True, (255, 255, 255))
        screen.blit(text1, (760, 542))
        screen.blit(text2, (560, 660))
    pygame.display.flip()