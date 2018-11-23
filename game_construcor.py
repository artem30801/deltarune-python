from game_functions import *

pygame.mixer.music.load(os.path.join('music', 'fofdr' + '.mp3'))
pygame.mixer.music.play()

kris = Chara("kris_w_d")
dialog1 = Speech("Avoid tree, bud", "arial", "lanc_dank", "talk_default", 3)
dialog2 = Speech("Thus is NOT your home", "arial", "lanc_dank", "talk_default", 3)


tree1 = Obstacle(400, 300, "tree_d_r", boundary=(130, 320, 130, 50))
nottree = Obstacle(100, 0, "blookhouse", boundary=(0, 200, 183, 58))

trig1 = InteractTrigger(tree1, dialog1)
trig2 = InteractTrigger(nottree, dialog2)

#activate_dialog(dialog1)
