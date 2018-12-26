from game_functions import *

kris_walk = LoadedImages("characters", "kris_w_d", 16)
ralsei_walk = LoadedImages("characters", "ralsei_w_d", 16, colorkey=None)

dark_tree = LoadedImages("env", "tree_d_r", scale2x=False)
boombox = LoadedImages("env", "boombox", 2)
blook_house = LoadedImages("env", "blookhouse")
candy_tree = LoadedImages("env", "candy")
tiles_df = LoadedImages("env\\tiles\\dark_forest", "tile", 27)
lancer_dank = LoadedImages("dialog", "lanc_dank")
heart = LoadedImages("env", "heart")
sale = LoadedImages("env", "sale")
sales = LoadedImages("env", "sales")
housesss = LoadedImages("env", "housesss")
darkgrass = LoadedTile("darkgrass", 9, False)
dd = LoadedTile("dark", 1, True)
m1 = LoadedTile("m",1,True)
m2 = LoadedTile("m2",1,True)
m3 = LoadedTile("m3",1, True)
m4 = LoadedTile("m4",1,True)
m5 = LoadedTile("m5",1,True)
void_obstacle = LoadedTile(None, 1, True)
void_empty = LoadedTile(None, 1, False)
rarara = LoadedImages("dialog", "rarara")
sansa = LoadedImages("dialog","sansa")
gangsta = LoadedImages("env", "gangsta")

portal_sound = LoadedSound("snd_phone")
text_sound_default = LoadedSound("talk_default")

Silence = MusicPlayer(None)
FieldOfHopesAndDreams = MusicPlayer("13. Field of Hopes and Dreams")
April2012 = MusicPlayer("27. April 2012")
LancerMusic = MusicPlayer("9. Lancer")
napsti = MusicPlayer("napst", 1)

dtm_mono = LoadedFont("DTM-Mono")

ob = void_obstacle
no = void_empty
gr = darkgrass

lvl1_disign = [[18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23],
               [24, 25, 25, 25, 22, 22, 22, 22, 25, 25, 25, 26],
               [ob, ob, ob, ob, 15, 22, 22, 17, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 22, 1, 1, 1, 1, 1],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, 21, 23, ob, ob, ob, ob, ob],
               [1, 1, 1, 1, 1, 25, 25, 1, 1, 1, 1, 1],
               [ob, ob, ob, ob, ob, no, no, ob, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, no, no, ob, ob, ob, ob, ob]]

lvl2_disign = [[no, no, no, no, no, no, no, no, no, no],
               [ob, ob, ob, ob, ob, no, no, no, no, no],
               [1 , 1 , 1 , 2 , ob, no, no, no, no, no],
               [ob, ob, ob, 6 , ob, 18, 20, no, no, no],
               [ob, ob, ob, 6 , ob, 24, 26, no, no, no],
               [1 , 1 , 1 , 14, ob, no, no, no, no, no],
               [ob, ob, ob, ob, ob, no, no, no, no, no],
               [no, no, no, no, no, no, no, no, no, no]]

lvl3_disign = [[ob, 3, 5, ob, ob, ob, ob, 3, 5, ob],
               [3, 22, 22, 5, ob, ob, 3, 22, 22, 5],
               [21, 22, 22, 22, 19, 19, 22, 22, 22, 23],
               [15, 22, 22, 22, 22, 22, 22, 22, 22, 17],
               [ob, 15, 22, 22, 22, 22, 22, 22, 17, ob],
               [ob, ob, 15, 22, 22, 22, 22, 17, ob, ob],
               [ob, ob, ob, 15, 22, 22, 17, ob, ob, ob],
               [ob, ob, ob, ob, 21, 23, ob, ob, ob, ob],
               [ob, ob, ob, ob, 21, 23, ob, ob, ob, ob],
               [9, 1, 1, 1, 25, 25, 1, 1, 1, 1]]
lvl4 = [[ob,ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [m5, ob, ob, ob, no, no, ob, ob, m2, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, dd, ob, ob, ob],
        [ob, ob, m2, ob, no, no, ob, ob, m2, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [dd, ob, ob, ob, no, no, ob, ob, m3, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, m4, ob, ob],
        [ob, ob, ob, ob, no, no, dd, ob, ob, ob],
        [ob, m3, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, m2, ob, ob],
        [dd, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, m3, ob, no, no, ob, ob, ob, m4],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, dd, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, m3, ob, ob, no, no, ob, m4, ob, ob],
        [dd, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [m2, ob, ob, ob, no, no, ob, ob, ob, m3],
        [ob, ob, ob, ob, no, no, dd, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, m5, ob, ob, no, no, m3, ob, ob, ob],
        [dd, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
        [ob, ob, ob, ob, ob, ob, ob, m4, ob, ob]]

room1 = Room(960, 1040, FieldOfHopesAndDreams)
room2 = Room(800, 640, FieldOfHopesAndDreams)
room3 = Room(800, 800, FieldOfHopesAndDreams)
hous = Room(490,450,napsti, housesss)
room4 = Room(800, 2400, napsti)

room1.generate_floor(lvl1_disign, tiles_df)
room2.generate_floor(lvl2_disign, tiles_df)
room3.generate_floor(lvl3_disign, tiles_df)
room4.generate_floor(lvl4, tiles_df)

kris = Chara(kris_walk)
kris.set_position(480, 100)
ralsei = Follower(ralsei_walk, kris)
ralsei.activate()  # activate follow-mode
#ralsei1 = Follower(kris_walk, ralsei)
#ralsei1.activate()
character_list.add(kris, ralsei)

tree1 = Obstacle(dark_tree, (550, 100), (65, 160, 65, 25))
boombox = Obstacle(boombox, (400, 300), (0, 0, 80, 80), 10)
blookhouse = Obstacle(blook_house, (100, 0), (0, 200, 183, 58))
cantr = Obstacle(candy_tree, (436, 180), (0, 0, 80, 80))
heart = Obstacle(heart, (10, 740), (0, 0, 30, 60))
sale = Obstacle(sale, (100, 80), (0, 0, 108, 166))
sales = Obstacle(sales, (580, 80), (0, 0, 108, 166))
gangsta = Obstacle(gangsta, (360,120), (0,0, 48, 80))

test_box = DialogSpeech(["/rDetermination /oBravery", "/yJustice /gKindness /aPatience", "/bIntegrity /vPerseverance"],
                        dtm_mono, None, text_sound_default)
test_box1 = DialogSpeech(["/wYou know...", "I've got all of them!", "ahahhah"],
                         dtm_mono, lancer_dank, text_sound_default)
b1 = DialogSpeech(["/wDo you remember this?"], dtm_mono,rarara, text_sound_default)
b2 = DialogSpeech(["This is your /rsoul/w,", "the very culmination" ,"of your being."],dtm_mono,rarara, text_sound_default)
b3 = DialogSpeech(["/rAND YOU LEFT IT"], dtm_mono, sansa, text_sound_default, 9)
b4 = DialogSpeech(["oh hello", "i'm sorry but i'm busy now", 'come later'],dtm_mono, None, text_sound_default, 1)
b5 = DialogSpeech(["yes come later", "oh don't force yourself", "oh no oh no"],dtm_mono, None, text_sound_default, 1)

dialog1 = Dialog(test_box, test_box1, music=LancerMusic)
dialog2 = Dialog(b1, b2,b3, music = Silence)
dialog3 = Dialog(b4, b5, music = napsti)

room1.bind(tree1, blookhouse)
room2.bind(boombox, cantr)
room3.bind(heart, sale, sales)
hous.bind(gangsta)

portal12 = RoomPortalStep(room1, room2, (30, 120), (950, 560, 10, 80), portal_sound)
portal122 = RoomPortalStep(room1, room2, (30, 360), (950, 800, 10, 80), portal_sound)
portal21 = RoomPortalStep(room2, room1, (880, 520), (-70, 160, 10, 80), portal_sound)
portal212 = RoomPortalStep(room2, room1, (880, 760), (-70, 400, 10, 80), portal_sound)
portal13 = RoomPortalStep(room1, room3, (720, 690), (-70, 800, 10, 80), portal_sound)
portal31 = RoomPortalStep(room3, room1, (30, 770), (790, 720, 10, 80), portal_sound)
portal1h = RoomPortal(room1, hous, (80,330), portal_sound)
portalh1 = RoomPortalStep(hous, room1, (205, 210), (80, 420, 160, 10), portal_sound)
portal14 = RoomPortalStep(room1, room4, (400, 100), (480,1000,160,10), portal_sound)
portal41 = RoomPortalStep(room4, room1, (480,900), (400, 20, 160, 10), portal_sound)

trig1 = InteractTrigger(dialog1, tree1)
trig2 = InteractTrigger(portal1h, blookhouse)
trig3 = InteractTrigger(dialog2, heart)
trig4 = InteractTrigger(dialog3, gangsta)




room1.bind_triggers(trig2)
room1.bind_triggers(trig1)
room3.bind_triggers(trig3)
hous.bind_triggers(trig4)

room1.activate()
