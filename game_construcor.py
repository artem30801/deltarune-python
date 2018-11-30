from game_functions import *
kris_walk = LoadedImages("characters", "kris_w_d", 16)

dark_tree = LoadedImages("env", "tree_d_r", scale2x=False)
boombox = LoadedImages("env", "boombox", 2)
blook_house = LoadedImages("env", "blookhouse", 1)

tiles_df = LoadedImages("env\\tiles\\dark_forest", "tile", 27)

portal_sound = LoadedSound("snd_phone")

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
               [1 , 1 , 1 , 1 , 1 , 25, 25, 1 , 1 , 1 , 1 , 1 ],
               [ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob]]

room1 = Room(960, 960, "fofdr")
room2 = Room(800, 600, "27. April 2012")

kris = Chara(kris_walk)
dialog1 = Speech("Avoid tree, bud", "DTM-Mono", "lanc_dank", "talk_default", 3)
dialog2 = Speech("Thus is NOT your home", "DTM-Mono", "lanc_dank", "talk_default", 3)
dialog3 = Speech("Such a sweet music", "DTM-Mono", "lanc_dank", "talk_default", 3)

dialogsss = Dialog(dialog1, dialog2, dialog3)

tree1 = Obstacle(dark_tree, (550, 100), (65, 160, 65, 25))
boombox = Obstacle(boombox, (400, 300), (0, 0, 80, 80), 10, 2)

blookhouse = Obstacle(blook_house, (100, 0), (0, 200, 183, 58))


room1.bind(kris, tree1, blookhouse)
room2.bind(kris, boombox)

portal12 = RoomPortalStep(room1, room2, (100, 300), (950, 560, 10, 80), portal_sound)
portal21 = RoomPortalStep(room2, room1, (870, 555), (0, 300, 10, 80), portal_sound)


trig1 = InteractTrigger(dialogsss, tree1)
trig2 = InteractTrigger(dialog2, blookhouse)
trig3 = InteractTrigger(dialog3, boombox)

room1.bind_triggers(trig1, trig2)
room2.bind_triggers(trig3)

room1.generate_floor(lvl1_disign, tiles_df)
room1.activate()
