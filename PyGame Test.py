# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math



ch = 0
pygame.init()
SIZE_SCREEN = SIZE_LENGTH, SIZE_HEIGHT = 1920, 1020
screen = pygame.display.set_mode(SIZE_SCREEN)
fon = pygame.transform.scale(pygame.image.load("/Users/a1/PycharmProjects/pythonProject1/WhiteCorrect.jpeg"), (1920, 1080))




main_running = True
while main_running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_running = False


    screen.blit(fon, (0, 0))
    pygame.display.flip()


