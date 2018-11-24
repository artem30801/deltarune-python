from game_functions import *

room1 = Room(1000, 1000, "fofdr")
room2 = Room(800, 600, "fofdr")

kris = Chara("kris_w_d")
dialog1 = Speech("Avoid tree, bud", "arial", "lanc_dank", "talk_default", 3)
dialog2 = Speech("Thus is NOT your home", "arial", "lanc_dank", "talk_default", 3)
dialog3 = Speech("Seems like another tree", "arial", "lanc_dank", "talk_default", 3)


tree1 = Obstacle(400, 300, "tree_d_r", boundary=(130, 320, 130, 50))
tree2 = Obstacle(200, 200, "tree_d_r", boundary=(130, 320, 130, 50))

nottree = Obstacle(100, 0, "blookhouse", boundary=(0, 200, 183, 58))

room1.bind(kris, tree1, nottree)
room2.bind(kris, tree2)


trig1 = InteractTrigger(dialog1, tree1)
trig2 = InteractTrigger(room2, nottree)
trig3 = InteractTrigger(dialog3, tree2)


room1.activate()
