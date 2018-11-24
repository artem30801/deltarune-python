import pygame
import os
import wave
from pygame.locals import *

# Init pygame itself
pygame.init()

# Init sound
file_wav = wave.open(os.path.join('SFX', "talk_default" + '.wav'))
frequency = file_wav.getframerate()
pygame.mixer.init(frequency=frequency)

# Init basic variables
ALPHA = (0, 0, 0)

WIDTH = 800
HEIGHT = 600

lvl_width = 1200
lvl_height = 1200

# Init window
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Init screens
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = screen.copy()

pygame.display.set_caption("SURVEY_PROGRAM")
icon = pygame.image.load(os.path.join('images', 'icon' + '.jpg')).convert()
pygame.display.set_icon(icon)

# Tick-tock clock
FPS = 30
time = pygame.time.Clock()