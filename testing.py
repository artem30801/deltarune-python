from tkinter import *
import pygame
from pygame.locals import *
pygame.init()
root = Tk()
#label = Label(text='I CAN DO ANYTHING! CHAOS CHAOS!', font=('Times','30'), fg='black', bg='white')
label = Label(root, bg='white')
label.jevil = PhotoImage(file="jevil.png")
label['image'] = label.jevil
label.master.overrideredirect(True)
label.master.lift()

label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)
label.master.wm_attributes("-transparentcolor", "white")
label.pack()

posx = 0
posy = 300
#screen = pygame.display.set_mode((600, 800), NOFRAME)
FPS = 30
time = pygame.time.Clock()

s = ""
if s:
    print(1)
else:
    print(2)
while True:
    #label.draw()
    posx+=1
    pos = "+"+str(posx)+"+"+str(posy)
    label.master.geometry(pos)

    root.update_idletasks()
    root.update()
    time.tick(FPS)

