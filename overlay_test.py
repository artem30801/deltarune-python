import pygame
import time
W = 352
H = 288
WH = (W, H)

pygame.init()
screen = pygame.display.set_mode((300, 300))

#overlay = pygame.Overlay(pygame.YV12_OVERLAY, WH)

fd = open('foreman_cif.yuv', 'rb')
y = fd.read(W * H)
u = fd.read(W * H // 4)
v = fd.read(W * H // 4)

overlay = pygame.Overlay(pygame.YV12_OVERLAY, (W, H))

overlay.set_location((-100, 200, W, H))

overlay.display((y, u, v))

time.sleep(5)
