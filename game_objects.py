from game_init import * #TODO all datatypes in funcions :int etc
import config

character_list = pygame.sprite.Group()
dialog_layer = pygame.sprite.Group()
active_animations = []


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)


def get_empty_image(empty_size=(80, 80), colorkey=pygame.color.Color("black")):
    image = pygame.Surface(empty_size)
    image.fill(colorkey)
    image.set_colorkey(ALPHA)
    return image


def convert_to_colorkey_alpha(surf, colorkey=pygame.color.Color("magenta")):
    newsurf = pygame.Surface(surf.get_size())
    newsurf.fill(colorkey)
    newsurf.blit(surf, (0, 0))
    newsurf.set_colorkey(colorkey)
    return newsurf


class MusicPlayer:
    current_music = None
    previous_music = None
    previous_time = 0

    def __init__(self, music_name, ext=".mp3"):
        self.music = music_name
        self.ext = ext

    def play(self):
        if MusicPlayer.current_music != self:
            MusicPlayer.previous_music = MusicPlayer.current_music
            MusicPlayer.previous_time = 0
            if MusicPlayer.current_music is not None:
                MusicPlayer.previous_time = pygame.mixer.music.get_pos()
            pygame.mixer.music.stop()
            if self.music is not None:
                pygame.mixer.music.load(os.path.join('music', self.music + self.ext))
                pygame.mixer.music.play(-1)
        MusicPlayer.current_music = self

    @staticmethod
    def play_previous():
        if MusicPlayer.current_music != MusicPlayer.previous_music:
            MusicPlayer.current_music, MusicPlayer.previous_music = \
                MusicPlayer.previous_music, MusicPlayer.current_music
            prev_time = MusicPlayer.previous_time
            if MusicPlayer.current_music.music is not None:
                MusicPlayer.previous_time = pygame.mixer.music.get_pos()

            pygame.mixer.music.stop()
            if MusicPlayer.current_music is not None:
                pygame.mixer.music.load(os.path.join('music', MusicPlayer.current_music.music + '.mp3'))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_pos(prev_time/1000)


class LoadedImages:
    def __init__(self, img_folder, img_name, count=1, scale2x=True, empty_size=(40, 40)):
        self.count = count
        self.images = []
        for i in range(self.count):
            if img_name is not None:
                image = pygame.image.load(
                    os.path.join('images', img_folder, img_name + str(i+1) + '.png')).convert_alpha()
                image = convert_to_colorkey_alpha(image)
            else:
                image = get_empty_image(empty_size)
            if scale2x:
                image = pygame.transform.scale2x(image)
            self.images.append(image)
        self.image = self.images[0]


class LoadedTile(LoadedImages):
    def __init__(self, img_name, count=1, isobstacle=False, scale2x=True):
        super().__init__("env/tiles", img_name, count, scale2x)
        self.isobstacle = isobstacle


class LoadedSound:
    def __init__(self, sound_name):
        self.sound = pygame.mixer.Sound(os.path.join('SFX', sound_name + '.wav'))

    def activate(self):
        self.sound.play()


class LoadedFont:
    def __init__(self, font_name, size=36):
        self.font = pygame.font.Font(os.path.join('fonts', font_name + '.otf'), size)


class Room:
    current_room = None
    rooms_dict = {}

    def __init__(self, name: str, music: MusicPlayer = None, width: int = WIDTH, height: int = HEIGHT, background_image: LoadedImages = None):  # Fix order
        self.width = width
        self.height = height
        self.music = music

        self.name = name
        Room.rooms_dict[self.name] = self

        self.triggers_list = []

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacle_list = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        self.camera_screen = pygame.Surface((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        if background_image is not None:
            self.background.blit(background_image.image, (0, 0))

    def generate_floor(self, tiles_map, tiles=None, back_color=(0, 0, 0)):
        self.background.fill(back_color)
        images = tiles.images

        for y, row in enumerate(tiles_map):
            for x, tile in enumerate(row):
                if isinstance(tile, LoadedTile):
                    obj = Tile(tile, (x * 80, y * 80), (0, 0, 80, 80))
                    self.background_sprites.add(obj)
                    if obj.isobstacle:
                        self.obstacle_list.add(obj)
                else:
                    self.background.blit(images[tile], (x * 80, y * 80))

    def load_tmx(self, filename):
        tm = load_pygame("tmx/"+filename+".tmx")
        self.width, self.height = tm.width * tm.tilewidth, tm.height * tm.tileheight
        if tm.background_color:
            self.background.fill(pygame.Color(tm.background_color))
        tw = tm.tilewidth
        th = tm.tileheight
        for layer in tm.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.background.blit(image, (x * tw, y * th))
            if isinstance(layer, TiledObjectGroup):
                for obj in layer:
                    if obj.type == 'obstacle':
                        obstacle = Obstacle(None, position=(obj.x, obj.y), boundary=(0, 0, obj.width, obj.height))
                        obstacle.add(self.all_sprites, self.obstacle_list)
                    elif obj.type == 'portal':
                        room2 = Room.rooms_dict[obj.properties['dest_room']]
                        portal = RoomPortalStep(self, room2,
                                                tp_position=(obj.properties['dest_x'], obj.properties['dest_y']),
                                                position=(obj.x, obj.y, obj.width, obj.height))

    def bind(self, *game_objects):
        for obj in game_objects:
            self.all_sprites.add(obj)
            if isinstance(obj, Obstacle):
                self.obstacle_list.add(obj)

    def bind_triggers(self, *triggers):
        self.triggers_list.extend(triggers)

    def activate(self):
        for obj in character_list:
            self.all_sprites.add(obj)

        Room.current_room = self
        self.music.play()


class RoomPortal:
    def __init__(self, room1, room2, tp_position=(0, 0), sound=None):
        self.room1 = room1
        self.room2 = room2

        self.tp_position = tp_position
        self.fadeout = AnimateAlpha(15, 255, alpha_surface, on_done=self.portal)
        self.fadein = AnimateAlpha(15, 0, alpha_surface, on_done=self.done)

        self.sound = None
        if sound is not None:
            self.sound = sound.sound

        self.active = False

    def activate(self):
        if not self.active:
            if self.sound is not None:
                self.sound.play()
            self.fadeout.activate()
        self.active = True

    def portal(self):
        if self.room1 is not self.room2:
            self.room2.activate()
        for character in character_list:
            character.rect.topleft = self.tp_position
            if isinstance(character, Follower):
                character.reset_path()
        self.fadein.activate()

    def done(self):
        self.active = False


class RoomPortalStep(RoomPortal):
    def __init__(self, room1, room2, tp_position=(0, 0), position=(0, 0, 80, 80), sound_name=None):
        super().__init__(room1, room2, tp_position, sound_name)
        self.position = position
        portal = GameObj(None, position=(position[0], position[1]), empty_size=(position[2], position[3]))
        trigger = StepOnTrigger(self, portal)
        room1.bind(portal)
        room1.bind_triggers(trigger)


class GameObj(pygame.sprite.Sprite):
    def __init__(self, image, position=(0, 0), animation_cycle=3, speed=7, empty_size=(80, 80)):
        pygame.sprite.Sprite.__init__(self)

        self.movex = 0
        self.movey = 0
        self.position = position

        self.speed = speed

        self.frame = 0
        self.animation_cycle = animation_cycle

        self.images = []
        if image is not None:
            self.images = image.images
            self.sprite_count = image.count
        else:
            self.images.append(get_empty_image(empty_size))
            self.sprite_count = 1

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=position)
        self._layer = self.rect.bottom

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def control_speed(self, dx, dy):
        self.movex += dx
        self.movey += dy

    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.frame >= self.sprite_count*self.animation_cycle:
            self.frame = 0

        self.image = self.images[(self.frame // self.animation_cycle)]
        self.frame += 1

        Room.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Chara(GameObj):
    def __init__(self, walk_images):
        super().__init__(walk_images, animation_cycle=3)
        self.frame_offset = 0

        self.boundary = (0, self.rect.height-15, self.rect.width, 15)

        self.footprint_rect = pygame.rect.Rect((self.boundary[0] + self.rect.x,
                                                self.boundary[1] + self.rect.y,
                                                self.boundary[2], self.boundary[3]
                                                ))

        self.vicinity_rect = self.rect.inflate(2, 2)
        self.vicinity_rect.center = self.rect.center

    def update(self):
        # undo movement if collide
        self.rect.x += self.movex*self.speed
        self.footprint_rect.midbottom = self.rect.midbottom
        while self.check_collisions()[0]:
            self.rect.x = self.rect.x - self.movex // abs(self.movex)
            self.footprint_rect.midbottom = self.rect.midbottom

        self.rect.y += self.movey*self.speed
        self.footprint_rect.midbottom = self.rect.midbottom
        while self.check_collisions()[1]:
            self.rect.y = self.rect.y - self.movey//abs(self.movey)
            self.footprint_rect.midbottom = self.rect.midbottom

        self.change_image(self.movex, self.movey)

        self.vicinity_rect.center = self.rect.center

        Room.current_room.all_sprites.change_layer(self, self.rect.bottom)

    def change_image(self, movex, movey):
        if self.frame >= 4 * self.animation_cycle:
            self.frame = 0

        if movey > 0:
            self.frame_offset = 0
        if movey < 0:
            self.frame_offset = 12
        if movex > 0:
            self.frame_offset = 4
        if movex < 0:
            self.frame_offset = 8

        if movex == 0 and movey == 0:
            self.frame = 0
        self.image = self.images[(self.frame // self.animation_cycle) + self.frame_offset]

        if movex != 0 or movey != 0:
            self.frame += 1

    def check_collisions(self):
        collide_x = False
        collide_y = False
        for obstacle in Room.current_room.obstacle_list:
            if self.footprint_rect.colliderect(obstacle.footprint_rect):
                if self.movex != 0:
                    collide_x = True
                if self.movey != 0:
                    collide_y = True
        # collide with room border
        if self.rect.x < 0 or self.rect.right > Room.current_room.width:
            collide_x = True
        if self.rect.y < 0 or self.rect.bottom > Room.current_room.height:
            collide_y = True
        return collide_x, collide_y


class Follower(Chara):
    def __init__(self, walk_images, target, path_length=15):
        super().__init__(walk_images)
        self.target = target
        self.active = False
        self.path_length = path_length
        self.walk_path = []
        self.reset_path()

    def activate(self):
        self.active = not self.active

    def reset_path(self):
        self.walk_path = [self.target.rect.midbottom for i in range(self.path_length)]

    def update(self):
        movex, movey = 0, 0
        if self.active:
            if self.target.rect.midbottom != self.walk_path[-1]:
                self.walk_path.append(self.target.rect.midbottom)
            if get_distance(self.footprint_rect.midbottom[0], self.footprint_rect.midbottom[1],
                            self.target.footprint_rect.midbottom[0], self.target.footprint_rect.midbottom[1]) > 70:
                target_pos = self.walk_path.pop(0)
                if len(self.walk_path) >= self.path_length:
                    self.walk_path.pop(0)
                movex = target_pos[0] - self.rect.midbottom[0]
                movey = target_pos[1] - self.rect.midbottom[1]

                self.rect.x += movex
                self.rect.y += movey
        self.footprint_rect.midbottom = self.rect.midbottom
        self.vicinity_rect.center = self.rect.center

        self.change_image(movex, movey)
        Room.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Obstacle(GameObj):
    def __init__(self, image, position=(0, 0), boundary=(0, 0, 80, 80), animation_cycle=1):
        super().__init__(image, position, animation_cycle)

        self.boundary = boundary

        self.footprint_rect = pygame.rect.Rect((self.boundary[0] + self.rect.x,
                                                self.boundary[1] + self.rect.y,
                                                self.boundary[2], self.boundary[3]
                                                ))

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        if self.frame >= self.sprite_count*self.animation_cycle:
            self.frame = 0

        self.image = self.images[(self.frame // self.animation_cycle)]
        self.frame += 1

        self.footprint_rect.x = self.rect.x + self.boundary[0]
        self.footprint_rect.y = self.rect.y + self.boundary[1]
        Room.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Tile(Obstacle):
    def __init__(self, tile, position=(0, 0), boundary=(0, 0, 80, 80), animation_cycle=4):
        super().__init__(tile, position, boundary, animation_cycle)
        self.isobstacle = tile.isobstacle

    def update(self):
        if self.movex != 0 and self.movey != 0:
            self.rect.x += self.movex
            self.rect.y += self.movey
            self.footprint_rect.x = self.rect.x + self.boundary[0]
            self.footprint_rect.y = self.rect.y + self.boundary[1]

        if self.frame >= self.sprite_count * self.animation_cycle:
            self.frame = 0

        self.image = self.images[(self.frame // self.animation_cycle)]
        self.frame += 1


class Dialog:
    current_dialog = None

    def __init__(self, *speech, music=None, repeatable=True):
        self.speeches = speech
        self.count = len(self.speeches)
        self.current = 0
        self.repeatable = repeatable
        self.music = music

    def activate(self):
        Dialog.current_dialog = self
        config.game_state = "dialog"
        if self.music is not None:
            self.music.play()
        self.skip()

    def choice(self, direction):
        pass

    def next(self):
        #test if able to skip
        if self.speeches[self.current-1].done:
            self.skip()

    def skip(self):
        if self.current >= self.count:
            self.end()
        else:
            if self.current > 0:
                self.speeches[self.current-1].reset()
            self.speeches[self.current].activate()
            self.current += 1

    def end(self):
        self.speeches[self.current-1].reset()
        config.game_state = "overworld"
        Dialog.current_dialog = None
        if self.music is not None:
            MusicPlayer.play_previous()
        if self.repeatable:
            self.current = 0


class DialogBox(pygame.sprite.Sprite):  # Baisic class, do not call directly
    def __init__(self, font, position=(20, 400), size=(760, 180)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font.font
        self.done = False

        self.rect = pygame.Rect(position, size)
        self.image = self.draw_all()
        #self.draw_textbox(["Heya. ... ", "So, i've got a question for ya.", "Do you think even the worst person can change. . . ?"], ((10, 10), size))

    def draw_border(self):
        border_surface = pygame.Surface(self.rect.size)
        border_surface.fill((0, 0, 0))
        lines_width = 4
        pygame.draw.rect(border_surface, (255, 255, 255),
                         (lines_width//2, lines_width//2, self.rect.width - lines_width, self.rect.height - lines_width), lines_width)
        return border_surface

    def draw_textbox(self, lines, rect, text_color=(255, 255, 255), aa=False):
        rect = pygame.Rect(rect)
        y = rect.top
        line_spacing = -2
        font_height = self.font.size("Tg")[1]
        for line in lines:
            while line:
                i = 1
                if y + font_height > rect.bottom:
                    break
                while self.font.size(line[:i])[0] < rect.width and i < len(line):
                    i += 1
                if i < len(line):
                    i = line.rfind(" ", 0, i) + 1
                text_surf = self.font.render(line[:i], aa, text_color)
                self.image.blit(text_surf, (rect.left, y))
                y += font_height + line_spacing
                line = line[i:]

    def draw_all(self):
        surface = self.draw_border()
        return surface

    def activate(self):
        dialog_layer.add(self)

    def reset(self):
        self.kill()


class DialogSpeech(DialogBox):
    def __init__(self, lines, font, face_image=None, sound=None, speed=3, autoplay=False):
        self.face = None
        super().__init__(font)

        self.frame = 0
        self.speed = speed
        self.autoplay = autoplay

        self.inp_lines = lines[:]
        self.lines = lines

        if sound is not None:
            self.sound = sound.sound
        if face_image is not None:
            self.face = pygame.transform.scale(face_image.image, (160, 160))
            self.text_rect = pygame.Rect((170, 20), (620, 140))
            #self.image.blit(self.face, (10, 10))
        else:
            self.face = None
            self.text_rect = pygame.Rect((20, 20), (720, 140))

        self.x = 0
        self.y = 0

        self.current_color = (255, 255, 255)
        self.image = self.draw_all()

    def draw_all(self):
        surface = self.draw_border()
        if self.face is not None:
            surface.blit(self.face, (10, 10))
        return surface

    def normalize_lines(self):  # todo перенос строк - разбиение списка по ширине строки
        line_width = self.font.size(self.lines[self.y])[0]

    def update(self, aa=False):
        if not self.done:
            if self.y < len(self.lines):
                if self.frame % self.speed == 0:
                    if self.lines[self.y][self.x] == "/":
                        command = self.lines[self.y][self.x+1]
                        self.lines[self.y] = self.lines[self.y][:self.x] + self.lines[self.y][self.x + 2:]
                        if command == "r":
                            self.current_color = (255, 0, 0)  # тут вложенный звиздец - 5 гребаных ифов
                        if command == "g":
                            self.current_color = (0, 255, 0)
                        if command == "b":
                            self.current_color = (0, 0, 255)
                        if command == "y":
                            self.current_color = (255, 255, 0)
                        if command == "a":
                            self.current_color = (0, 255, 255)
                        if command == "v":
                            self.current_color = (255, 0, 255)
                        if command == "o":
                            self.current_color = (255, 127, 0)
                        if command == "w":
                            self.current_color = (255, 255, 255)

                    line_spacing = -2
                    letter_spacing = 1
                    font_height = self.font.size("Tg")[1]
                    font_width = self.font.size(self.lines[self.y][self.x])[0]
                    text_surf = self.font.render(self.lines[self.y][self.x], aa, self.current_color)

                    self.image.blit(text_surf, (self.text_rect.left + self.x * (font_width + letter_spacing),
                                                self.text_rect.top + self.y * (font_height + line_spacing)))

                    if self.sound is not None:
                        if self.lines[self.y][self.x] != " ":
                            self.sound.play()

                    self.x += 1
                    if self.x >= len(self.lines[self.y]):
                        self.x = 0
                        self.y += 1
            else:
                self.done = True
                if self.autoplay:
                    Dialog.current_dialog.skip()
            self.frame += 1

    def reset(self):
        self.kill()
        self.done = False
        self.lines = self.inp_lines.copy()
        self.x = 0
        self.y = 0
        self.current_color = (255, 255, 255)
        self.image = self.draw_all()


class Choice:
    def __init__(self, choices_map):
        self.choice_actions = choices_map

        #if mapping is None:
        #    self.map = [i for i in range(len([self.choice_actions]))]
        #else:
        #    self.map = mapping #example of mapping:
        self.current_x = 0
        self.current_y = 0
        self.current_z = 0

    def change_choice(self):
        pass


class DialogChoice(DialogBox, Choice):  # TODO
    def __init__(self, *choice_texts, ):
        #super.__init__(DialogBox)
        pass


class Trigger:
    def __init__(self, result, once=False):
        self.counter = 0
        self.once = once

        self.result = result

    def check(self, event):
        pass

    def action(self):
        self.counter += 1
        if self.once:
            Room.current_room.triggers_list.remove(self)
        self.result.activate()


class InteractTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == ord('z'):
                if config.current_game.playable.vicinity_rect.colliderect(self.target.footprint_rect):
                    self.action()


class StepOnTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if config.current_game.playable.footprint_rect.colliderect(self.target.rect):
            self.action()


class Animation:
    def __init__(self, frames, target_value, target_obj, on_done=None, tweening=tween.linear):
        self.frames = frames
        self.current_frame = 0

        self.target_obj = target_obj
        self.target_value = target_value
        self.start_value = 0
        self.current_value = 0
        self.delta_value = 0

        self.tweening = tweening

        self.done = False
        self.on_done = on_done  # on done should be function or method!

    def activate(self):
        print("anim to", self.target_value)
        if self not in active_animations:  # защита от дурака(меня)
            self.start_value = self.get_current()
            self.delta_value = self.target_value - self.start_value
            active_animations.append(self)
        self.done = False

    def end(self):  # reseting all vars
        active_animations.remove(self)
        self.set_targets_value(self.target_value)
        self.current_frame = 0
        self.done = True
        print("end")

        if self.on_done is not None:
            return self.on_done()

    def action_frame(self):
        self.current_value = self.start_value + self.delta_value * self.tweening(self.current_frame/self.frames)
        self.current_frame += 1
        self.set_targets_value(self.current_value)
        if self.current_frame >= self.frames:
            self.end()

    def get_current(self):
        return 0

    def set_targets_value(self, value):
        pass


class AnimateAlpha(Animation):
    def get_current(self):
        obj = self.target_obj
        if isinstance(obj, list):
            obj = obj[0]
        val = obj.get_alpha()
        if val is not None:
            return val
        else:
            return 255

    def set_targets_value(self, value):
        if isinstance(self.target_obj, list):
            for image in self.target_obj:
                image.set_alpha(abs(value))
        else:
            self.target_obj.set_alpha(abs(value))


class AnimatePosition(Animation):
    def get_current(self):
        x, y = self.target_obj.rect.x, self.target_obj.rect.y
        return numpy.array((x, y), dtype=float)

    def set_targets_value(self, value):
        x, y = value
        self.target_obj.set_position(int(x), int(y))
