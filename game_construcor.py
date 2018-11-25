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
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [1, 1, 1, 1, 1, 25, 25, 1, 1, 1, 1, 1],
               [ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob]]

room1 = Room(960, 960, "fofdr")
room2 = Room(800, 600, "27. April 2012")

kris = Chara("kris_w_d")
dialog1 = Speech("Avoid tree, bud", "arial", "lanc_dank", "talk_default", 3)
dialog2 = Speech("Thus is NOT your home", "arial", "lanc_dank", "talk_default", 3)
dialog3 = Speech("Seems like another tree", "arial", "lanc_dank", "talk_default", 3)


tree1 = Obstacle("tree_d_r", (550, 0), (130, 320, 130, 50))
boombox = Obstacle("boombox", (400, 300), (0, 0, 80, 80), 10, 2)

blookhouse = Obstacle("blookhouse", (100, 0), boundary=(0, 200, 183, 58))

#boombox = GameObj("env", "boombox", 1, 2, position=(0, 0))

room1.bind(kris, tree1, blookhouse)
room2.bind(kris, boombox)

portal12 = RoomPortalStep(room1, room2, (100, 300), (950, 560, 10, 80), "snd_phone")
portal21 = RoomPortalStep(room2, room1, (870, 555), (0, 300, 10, 80), "snd_phone")


trig1 = InteractTrigger(dialog1, tree1)
trig2 = InteractTrigger(dialog2, blookhouse)
trig3 = InteractTrigger(dialog3, boombox)

room1.bind_triggers(trig1, trig2)
room2.bind_triggers(trig3)

room1.generate_floor(lvl1_disign, "dark_forest")
room1.activate()
