from game_functions import *
kris_walk = LoadedImages("characters", "kris_w_d", 16)
#rals_ei = LoadedImages("default_dance//ralsei","frame1", 2 )
dark_tree = LoadedImages("env", "tree_d_r", scale2x=False)
boombox = LoadedImages("env", "boombox", 2)
blook_house = LoadedImages("env", "blookhouse")
candy_tree = LoadedImages("env", "candy")

tiles_df = LoadedImages("env\\tiles\\dark_forest", "tile", 27)
lancer_dank = LoadedImages("dialog", "lanc_dank")

portal_sound = LoadedSound("snd_phone")

dtm_mono = LoadedFont("DTM-Mono")

ob = "ob"
no = "no"
lvl1_disign = [[18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [24, 25, 25, 25, 22, 22, 22, 22, 25, 25, 25, 26],
               [ob, ob, ob, ob, 15, 22, 22, 17, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 22, 1 , 1 , 1 , 1 , 1 ],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [1 , 1 , 1 , 1 , 1 , 25, 25, 1 , 1 , 1 , 1 , 1 ],
               [ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob, ob]]
lvl2_disign = [[no,no,no,no,no,no,no,no,no,no],
               [ob,ob,ob,ob,ob,no,no,no,no,no],
               [1 ,1 ,1 ,2 ,ob,no,no,no,no,no],
               [ob,ob,ob,6 ,ob,18,20,no,no,no],
               [ob,ob,ob,6 ,ob,24,26,no,no,no],
               [1 ,1 ,1 ,14,ob,no,no,no,no,no],
               [ob,ob,ob,ob,ob,no,no,no,no,no],
               [no,no,no,no,no,no,no,no,no,no]]
room1 = Room(960, 960, "fofdr")
room2 = Room(800, 640, "27. April 2012")

kris = Chara(kris_walk)
#dialog1 = Speech("Avoid tree, bud", "DTM-Mono", "lanc_dank", "talk_default", 3)
#dialog2 = Speech("Thus is NOT your home", "DTM-Mono", "lanc_dank", "talk_default", 3)
#dialog3 = Speech("Such a sweet music", "DTM-Mono", "lanc_dank", "talk_default", 3)

#dialogsss = Dialog(dialog1, dialog2, dialog3)

tree1 = Obstacle(dark_tree, (550, 100), (65, 160, 65, 25))
boombox = Obstacle(boombox, (400, 300), (0, 0, 80, 80), 10)
#ralsei = Obstacle(rals_ei,(500, 400), (0, 0, 80, 80), 10)
blookhouse = Obstacle(blook_house, (100, 0), (0, 200, 183, 58))

test_box = DialogSpeech(["Heya. ... ", "So, i've got a question for ya.", "Do you wanna have a bad time ?"], dtm_mono, lancer_dank, portal_sound)
cantr = Obstacle(candy_tree,(436, 180), (0, 0, 80, 80), 10 )
room1.bind(kris, tree1, blookhouse, test_box)
room2.bind(kris, boombox, cantr) #ralsei)

portal12 = RoomPortalStep(room1, room2, (30, 120), (950, 560, 10, 80), portal_sound)
portal122 = RoomPortalStep (room1, room2, (30,360),(950, 800, 10, 80), portal_sound)
portal21 = RoomPortalStep(room2, room1, (850, 540), (-70, 160, 10, 80), portal_sound)
portal212 = RoomPortalStep(room2, room1, (850, 760), (-70, 400, 10, 80), portal_sound)
#fade = AnimOverlay(10, False)
#fade.activate()


#trig1 = InteractTrigger(dialogsss, tree1)
#trig2 = InteractTrigger(dialog2, blookhouse)
#trig3 = InteractTrigger(dialog3, boombox)

#room1.bind_triggers(trig1, trig2)
#room2.bind_triggers(trig3)

room1.generate_floor(lvl1_disign, tiles_df)
room1.activate()
room2.generate_floor(lvl2_disign, tiles_df)