from game_functions import *
ob = "ob"
no = "no"
lvl1_disign = [[18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [24, 25, 25, 25, 22, 22, 22, 22, 25, 25, 25, 26],
               [ob, ob, ob, ob, 15, 22, 22, 17, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 22, no, no, no, no, no],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob]]

room1 = Room(960, 960, "fofdr")
room2 = Room(800, 600, "27. April 2012")

kris = Chara("kris_w_d")
dialog1 = Speech("Avoid tree, bud", "arial", "lanc_dank", "talk_default", 3)
dialog2 = Speech("Thus is NOT your home", "arial", "lanc_dank", "talk_default", 3)
dialog3 = Speech("Seems like another tree", "arial", "lanc_dank", "talk_default", 3)


tree1 = Obstacle("tree_d_r", (700, 100),  boundary=(130, 320, 130, 50))
tree2 = Obstacle( "tree_d_r", (200, 200), boundary=(130, 320, 130, 50))

nottree = Obstacle("blookhouse", (100, 0), boundary=(0, 200, 183, 58))


room1.bind(kris, tree1, nottree)
room2.bind(kris, tree2)

portal12 = RoomPortalStep(room1, room2, (100, 100), (880, 560, 80, 80), "snd_phone")

trig1 = InteractTrigger(dialog1, tree1)
trig2 = InteractTrigger(portal12, nottree)
trig3 = InteractTrigger(dialog3, tree2)

room1.bind_triggers(trig1, trig2)
room2.bind_triggers(trig3)

room1.generate_floor(lvl1_disign, "dark_forest")
room1.activate()
