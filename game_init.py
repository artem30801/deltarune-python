import math
import numpy
import os

from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

import pygame
from pygame.locals import *

import pytmx
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

import pytweening as tween


#Get user screen size
screensize = windll.user32.GetSystemMetrics(78), windll.user32.GetSystemMetrics(79)

# Init pygame itself
pygame.mixer.pre_init(44100, -16, 64, 1024)
pygame.init()
# Init sound

pygame.mixer.init(44100, -16, 64, 1024)


# Init basic variables
ALPHA = (0, 0, 0)

WIDTH = 800
HEIGHT = 600

# Init window
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Init screens
icon = pygame.image.load(os.path.join('images', 'icon' + '.jpg'))
icon = pygame.transform.smoothscale(icon, (32, 32))
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = screen.copy()
fake_screen.set_alpha(255)

alpha_surface = fake_screen.copy()
alpha_surface.fill((0, 0, 0))  # Fill it with whole black
alpha_surface.set_alpha(0)

pygame.display.set_caption("SURVEY_PROGRAM")

# Tick-tock clock
FPS = 30
time = pygame.time.Clock()
