# -*- coding: cp1251 -*-
import pygame
import copy
import os
import sys
import random
import math


def load_image(name, colorkey=None, convert=None):
    fullname = os.path.join("data", name)
    # ���� ���� �� ����������, �� �������
    if not os.path.isfile(fullname):
        print(f"���� � ������������ '{fullname}' �� ������")
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