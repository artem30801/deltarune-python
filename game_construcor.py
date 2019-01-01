from game_functions import *

# walk and actions
kris_walk = LoadedImages("characters", "kris_w_d", 16)
ralsei_walk = LoadedImages("characters", "ralsei_w_d", 16)

# dialog_faces
rarara = LoadedImages("dialog", "ralsei_face1-")
sansa = LoadedImages("dialog", "sans_face4-")
lancer_dank = LoadedImages("dialog", "lanc_dank")


dark_tree = LoadedImages("env", "tree_d_r", scale2x=False)
boombox = LoadedImages("env", "boombox", 2)
blook_house = LoadedImages("env", "blookhouse")
candy_tree = LoadedImages("env", "candy")
heart = LoadedImages("env", "heart")
sale = LoadedImages("env", "sale")
sales = LoadedImages("env", "sales")
napstablook = LoadedImages("env", "napstablook_front1-")
housesss = LoadedImages("env", "napstablook_house_inner2", scale2x=False)

# tiles ad tilesets
tiles_df = LoadedImages("env\\tiles\\dark_forest", "tile", 27)
darkgrass = LoadedTile("darkgrass", 9, False)
dd = LoadedTile("bg_darkstone_1-", 1, True, scale2x=False)
#m1 = LoadedTile("waterfall_lshoom1-", 1, True)
m2 = LoadedTile("waterfall_lshoom1-", 1, True)
m3 = LoadedTile("waterfall_lshoom2-", 1, True)
m4 = LoadedTile("waterfall_lshoom3-", 1, True)
m5 = LoadedTile("waterfall_lshoom4-", 1, True)
void_obstacle = LoadedTile(None, 1, True)
void_empty = LoadedTile(None, 1, False)


portal_sound = LoadedSound("snd_phone")
text_sound_default = LoadedSound("talk_default")

Silence = MusicPlayer(None)
FieldOfHopesAndDreams = MusicPlayer("13. Field of Hopes and Dreams")
April2012 = MusicPlayer("27. April 2012")
LancerMusic = MusicPlayer("9. Lancer")
sad_theme = MusicPlayer("renaissance_music")
napstablook_theme = MusicPlayer("napst", ".wav")

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
               [ob, ob, gr, ob, ob, no, no, no, no, no],
               [no, no, no, no, no, no, no, no, no, no]]

lvl3_disign = [[ob, 3, 5, ob, ob, ob, ob, 3, 5, ob],
               [3, 22, 22, 5, ob, ob, 3, 22, 22, 5],
               [21, 22, 22, 22, 19, 19, 22, 22, 22, 23],
               [15, 22, 22, 22, 22, 2, 22, 22, 22, 17],
               [ob, 15, 22, 22, 22, 22, 22, 22, 17, ob],
               [ob, ob, 15, 22, 22, 22, 22, 17, ob, ob],
               [ob, ob, ob, 15, 22, 22, 17, ob, ob, ob],
               [ob, ob, ob, ob, 21, 23, ob, ob, ob, ob],
               [ob, ob, ob, ob, 21, 23, ob, ob, ob, ob],
               [9, 1, 1, 1, 25, 25, 1, 1, 1, 1]]

lvl4_disign = [[ob, ob, ob, ob, no, no, ob, ob, ob, ob],
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
               [ob, ob, ob, ob, no, no, ob, m4, ob, ob],
               [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
               [m5, ob, ob, ob, no, no, ob, ob, m2, ob],
               [ob, ob, ob, ob, no, no, ob, ob, ob, ob],
               [ob, ob, ob, ob, ob, ob, dd, ob, ob, ob]]

napstablook_house_disign = [[ob, ob, ob, ob, ob, ob, ob, ob, ob, ob],
                            [ob, ob, ob, ob, ob, ob, ob, ob, ob, ob],
                            [ob, ob, no, no, no, no, no, ob, ob, ob],
                            [ob, ob, no, no, no, no, no, ob, ob, ob],
                            [ob, ob, no, no, no, no, no, ob, ob, ob],
                            [ob, ob, no, no, no, no, no, ob, ob, ob],
                            [ob, ob, no, no, ob, ob, ob, ob, ob, ob],
                            [ob, ob, no, no, ob, ob, ob, ob, ob, ob]]

room1 = Room(960, 1040, FieldOfHopesAndDreams)
room2 = Room(800, 640, FieldOfHopesAndDreams)
room3 = Room(800, 800, FieldOfHopesAndDreams)
blook_house_inside = Room(800, 600, napstablook_theme, housesss)
room4 = Room(800, 2400, sad_theme)

room1.generate_floor(lvl1_disign, tiles_df)
room2.generate_floor(lvl2_disign, tiles_df)
room3.generate_floor(lvl3_disign, tiles_df)
room4.generate_floor(lvl4_disign, tiles_df)
#blook_house_inside.generate_floor(napstablook_house_disign, tiles_df)


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
napstablook = Obstacle(napstablook, (360, 120), (0, 0, 48, 80))

obst1 = Obstacle(None, (0, 0), (0, 0, 140, 600))
obst2 = Obstacle(None, (0, 0), (0, 0, 800, 180))
obst3 = Obstacle(None, (600, 0), (0, 0, 140, 600))
obst4 = Obstacle(None, (250, 450), (0, 0, 550, 150))


test_box = DialogSpeech(["/rDetermination /oBravery", "/yJustice /gKindness /aPatience", "/bIntegrity /vPerseverance"],
                        dtm_mono, None, text_sound_default)
test_box1 = DialogSpeech(["/wYou know...", "I've got all of them!", "ahahhah"],
                         dtm_mono, lancer_dank, text_sound_default)
b1 = DialogSpeech(["/wDo you remember this?"], dtm_mono,rarara, text_sound_default)
b2 = DialogSpeech(["This is your /rsoul/w,", "the very culmination", "of your being."], dtm_mono, rarara, text_sound_default)
b3 = DialogSpeech(["/rAND YOU LEFT IT"], dtm_mono, sansa, text_sound_default, 9)
b4 = DialogSpeech(["/woh hello", "i'm sorry but i'm busy now", 'come later'], dtm_mono, None, text_sound_default, 1, True)
b5 = DialogSpeech(["yes come later", "oh don't force yourself", "oh no oh no"], dtm_mono, None, text_sound_default, 1, True)

dialog1 = Dialog(test_box, test_box1, music=LancerMusic)
dialog2 = Dialog(b1, b2, b3, music=Silence)
dialog3 = Dialog(b4, b5, music=None)

room1.bind(tree1, blookhouse)
room2.bind(boombox, cantr)
room3.bind(heart, sale, sales)
blook_house_inside.bind(napstablook, obst1, obst2, obst3, obst4)

portal12 = RoomPortalStep(room1, room2, (30, 120), (950, 560, 10, 80), portal_sound)
portal122 = RoomPortalStep(room1, room2, (30, 360), (950, 800, 10, 80), portal_sound)
portal21 = RoomPortalStep(room2, room1, (880, 520), (0, 160, 10, 80), portal_sound)
portal212 = RoomPortalStep(room2, room1, (880, 760), (0, 400, 10, 80), portal_sound)
portal13 = RoomPortalStep(room1, room3, (720, 690), (0, 800, 10, 80), portal_sound)
portal31 = RoomPortalStep(room3, room1, (30, 770), (790, 720, 10, 80), portal_sound)
portal1h = RoomPortal(room1, blook_house_inside, (160, 500), portal_sound)
portalh1 = RoomPortalStep(blook_house_inside, room1, (205, 210), (160, 590, 160, 10), portal_sound)
portal14 = RoomPortalStep(room1, room4, (400, 100), (480, 1000, 160, 10), portal_sound)
portal41 = RoomPortalStep(room4, room1, (480, 900), (0, 0, 600, 80), portal_sound)
portal44 = RoomPortalStep(room4, room4, (400, 200), (0, 2320, 600, 80), None)

trig1 = InteractTrigger(dialog1, tree1)
trig2 = InteractTrigger(portal1h, blookhouse)
trig3 = InteractTrigger(dialog2, heart)
trig4 = InteractTrigger(dialog3, napstablook)

room1.bind_triggers(trig1, trig2)
room3.bind_triggers(trig3)
blook_house_inside.bind_triggers(trig4)

room1.activate()

#just testing
anim_rls = AnimateAlpha(60, 3, ralsei.images, tweening=tween.easeOutBounce)
#anim_rls.activate()

window.update()
anim_pos = AnimatePosition(60, (0, 0), window, on_done=anim_rls.activate, tweening=tween.easeInExpo)
anim_pos.activate()
