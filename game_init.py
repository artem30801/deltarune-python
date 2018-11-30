import pygame
import os

import wave
from pygame.locals import *

# Init pygame itself
pygame.mixer.pre_init(44100, -16, 64, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 64, 1024)
pygame.init()

# Init sound
#file_wav = wave.open(os.path.join('SFX', "talk_default" + '.wav'))
#frequency = file_wav.getframerate()
#print(frequency)
#pygame.mixer.init(frequency=frequency)

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

pygame.display.set_caption("SURVEY_PROGRAM")

# Tick-tock clock
FPS = 30
time = pygame.time.Clock()
