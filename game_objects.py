from game_init import *
import config

dialog_layer = pygame.sprite.Group()
active_animations = []


def change_music(music_name=None):
    if config.current_music != music_name:
        config.previous_music = config.current_music
        pygame.mixer.music.stop()
        if music_name is not None:
            pygame.mixer.music.load(os.path.join('music', music_name + '.mp3'))
            pygame.mixer.music.play(-1)

    config.current_music = music_name


def get_empty_image(empty_size=(80, 80)):
    image = pygame.Surface(empty_size)
    image.set_colorkey(ALPHA)
    return image


class LoadedImages:
    def __init__(self, img_folder, img_name, count=1, scale2x=True, empty_size=(0, 0)):
        self.count = count
        self.images = []
        for i in range(self.count):
            if img_name is not None:
                image = pygame.image.load(
                    os.path.join('images', img_folder, img_name + str(i+1) + '.png')).convert()
                image.convert_alpha()
                image.set_colorkey(ALPHA)
            else:
                image = get_empty_image(empty_size)
            if scale2x:
                image = pygame.transform.scale2x(image)
            self.images.append(image)
        self.image = self.images[0]


class LoadedSound:
    def __init__(self, sound_name):
        self.sound = pygame.mixer.Sound(os.path.join('SFX', sound_name + '.wav'))


class LoadedFont:
    def __init__(self, font_name, size=36):
        self.font = pygame.font.Font(os.path.join('fonts', font_name + '.otf'), size)

class Room:
    def __init__(self, width, height, music=None):
        self.width = width
        self.height = height
        self.music = music

        self.triggers_list = []

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacle_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()

        self.camera_screen = pygame.Surface((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))

    def generate_floor(self, tiles_map, tiles, back_color=(0, 0, 0)):
        self.background.fill(back_color)
        images = tiles.images

        for y, row in enumerate(tiles_map):
            for x, tile in enumerate(row):
                if tile == "ob":
                    obstacle = Obstacle(None, (x * 80, y * 80), boundary=(0, 0, 80, 80))
                    self.bind(obstacle)
                elif tile == "no":
                    panel = pygame.Surface((80, 80))
                    panel.fill(back_color)
                    self.background.blit(panel, (x * 80, y * 80))
                else:
                    self.background.blit(images[tile], (x * 80, y * 80))

    def bind(self, *game_objects):
        for obj in game_objects:
            self.all_sprites.add(obj)
            if isinstance(obj, Obstacle):
                self.obstacle_list.add(obj)
            if isinstance(obj, Chara):
                self.character_list.add(obj)

    def bind_triggers(self, *triggers):
        self.triggers_list.extend(triggers)

    def activate(self):
        config.current_room = self

        change_music(self.music)


class RoomPortal:
    def __init__(self, room1, room2, tp_position=(0, 0), sound=None):
        self.room1 = room1
        self.room2 = room2

        self.tp_position = tp_position
        #self.fadeout = AnimOverlay(30, True)
        #self.fadein = AnimOverlay(30, False)

        self.sound = None
        if sound is not None:
            self.sound = sound.sound

    def activate(self):
        config.current_game.playable.rect.topleft = self.tp_position
        if self.sound is not None:
            self.sound.play()
        if config.current_room == self.room1:
            #self.fadeout.activate() сейчас функция не работает
            self.room2.activate()
            #self.fadein.activate() и эта тоже


class RoomPortalStep(RoomPortal):
    def __init__(self, room1, room2, tp_position=(0, 0), position=(0, 0, 80, 80), sound_name=None):
        super().__init__(room1, room2, tp_position, sound_name)
        self.position = position
        portal = GameObj(None, position=(position[0], position[1]))
        trigger = StepOnTrigger(self, portal)
        room1.bind(portal)
        room1.bind_triggers(trigger)


class GameObj(pygame.sprite.Sprite):
    def __init__(self, image, animation_cycle=1, speed=20,
                 position=(0, 0), empty_size=(80, 80)):
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
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self._layer = self.rect.bottom

    def control_speed(self, x, y):
        self.movex += x
        self.movey += y

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

        config.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Tile(GameObj):
    def __init__(self, image, animation_cycle=1, position=(0, 0)):
        super().__init__(image, animation_cycle, position=position)


class Chara(GameObj):
    def __init__(self, walk_images):
        super().__init__(walk_images, 3)

        self.boundary = (0, 70, 40, 15)

        self.footprint_rect = pygame.rect.Rect((self.boundary[0] + self.rect.x,
                                                self.boundary[1] + self.rect.y,
                                                self.boundary[2], self.boundary[3]
                                                ))

        self.vicinity_rect = self.rect.inflate(2,2)
        self.vicinity_rect.center = self.rect.center

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        self.footprint_rect.midbottom = self.rect.midbottom
        if self.frame >= 4 * self.animation_cycle:
            self.frame = 0

        frame_offset = 0
        if self.movey > 0:
            frame_offset = 0
        if self.movey < 0:
            frame_offset = 12
        if self.movex > 0:
            frame_offset = 4
        if self.movex < 0:
            frame_offset = 8

        if self.movex != 0 or self.movey != 0:
            self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]
            self.frame += 1

        collide_x = False
        collide_y = False
        for obstacle in config.current_room.obstacle_list:
            # collide = pygame.sprite.collide_mask(self, obstacle)
            if self.footprint_rect.colliderect(obstacle.footprint_rect):
                if self.movex != 0:
                    collide_x = True
                if self.movey != 0:
                    collide_y = True # collide with room border
        if self.rect.x < 0 or self.rect.right > config.current_room.width:
            collide_x = True
        if self.rect.y < 0 or self.rect.bottom > config.current_room.height:
            collide_y = True
        # undo movement if collide
        if collide_x:
            self.rect.x = self.rect.x - self.movex
        if collide_y:
            self.rect.y = self.rect.y - self.movey

        self.vicinity_rect.center = self.rect.center

        config.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Obstacle(GameObj):
    def __init__(self, image, position=(0, 0), boundary=(0, 0, 80, 80), animation_cycle=1):
        super().__init__(image, animation_cycle, position=position)

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
        config.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Dialog: #TODO test and music
    def __init__(self, *speech, repeatable=True, music=None):
        self.speeches = speech
        self.count = len(self.speeches)
        self.current = 0
        self.repeatable = repeatable

    def activate(self):
        config.current_dialog = self
        config.game_state = "dialog"
        self.skip()

    def next(self):
        #test if able to skip
        if self.speeches[self.current].frame // self.speeches[self.current].frame < len(self.speeches[self.current].frame):
            self.skip()

    def skip(self):
        if self.current >= self.count:
            self.end()
        if self.current > 0:
            self.speeches[self.current-1].reset()
        self.speeches[self.current].activate(standalone=False)
        self.current += 1

    def end(self):
        self.speeches[self.current-1].reset()
        config.game_state = "overworld"
        config.current_dialog = None

        if self.repeatable:
            self.current = 0


class DialogBox(pygame.sprite.Sprite):  # Baisic class, do not call directly
    def __init__(self, font, position=(20, 400), size=(760, 180)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font.font

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


class DialogSpeech(DialogBox):
    def __init__(self, lines, font, face_image=None, sound=None, speed=3):
        super().__init__(font)
        self.frame = 0
        self.speed = speed

        self.lines = lines

        if sound is not None:
            self.sound = sound.sound

        if face_image is not None:
            self.face = face_image.image
            self.text_rect = pygame.Rect((170, 20), (620, 140))
            self.image.blit(self.face, (10, 10))
        else:
            self.face = None
            self.text_rect = pygame.Rect((20, 20), (720, 140))

        self.x = 0
        self.y = 0

        self.current_color = (255, 255, 255)

    def normalize_lines(self):  # todo перенос строк - разбиение списка по ширине строки
        line_width = self.font.size(self.lines[self.y])[0]

    def update(self, aa=False):
        if self.y < len(self.lines):
            if self.frame % self.speed == 0:
                if self.lines[self.y][self.x] == "/":  # todo смена цвета печати по символу после слеша
                    pass
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
        self.frame += 1


class Speech(pygame.sprite.Sprite):
    def __init__(self, text, font_name, img_name, sound_name, speed=3, autoplay_time=0):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.Font(os.path.join('fonts', font_name + '.otf'), 36)
        self.size = 150

        self.frame = 0
        self.speed = speed
        self.autoplay = autoplay_time

        self.sound = pygame.mixer.Sound(os.path.join('SFX', sound_name + '.wav'))

        img = pygame.image.load(os.path.join('images\dialog', img_name + '.png')).convert()
        img = pygame.transform.scale(img, (self.size, self.size))
        img.convert_alpha()
        self.face = img

        self.image = self.draw_all()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT

    def draw_all(self):
        speech_height = 200
        speech_surface = pygame.Surface((WIDTH, speech_height))
        speech_surface.fill((0, 0, 0))
        lines_width = 4
        lines_points = [(0, 0), (WIDTH - lines_width, 0), (WIDTH - lines_width, speech_height - lines_width), (0, speech_height - lines_width)]
        pygame.draw.lines(speech_surface, (255, 255, 255), True, lines_points, lines_width*2)
        offset_y = speech_height//2 - self.size//2
        speech_surface.blit(self.face, (lines_width*2, offset_y))

        text_drawn = self.font.render(self.text[:self.frame//self.speed:], 0, (255, 255, 255))
        speech_surface.blit(text_drawn, (150, 20))

        return speech_surface

    def update(self):
        if self.frame % self.speed == 0:
            self.image = self.draw_all()
            if self.frame // self.speed < len(self.text):
                if self.text[self.frame//self.speed] != " ":
                    self.sound.play()
                    print(self.text[self.frame//self.speed])
        self.frame += 1

    def activate(self, standalone=True):
        if standalone:
            pygame.mixer.music.pause()
            config.game_state = "dialog"
        dialog_layer.add(self)

    def reset(self):
        dialog_layer.remove(self)
        self.frame = 0
        pygame.mixer.music.unpause()


class DialogChoice:  #TODO
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
            config.current_room.triggers_list.remove(self)
        self.result.activate()


class InteractTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if event.type == pygame.KEYUP:
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
    def __init__(self, frames, target):
        self.frames = frames

        self.target_value = target
        self.current_value = 0
        self.delta_value = 0

    def activate(self):
        active_animations.append(self)

    def end(self):
        active_animations.remove(self)

    def check(self):
        if self.current_value >= self.target_value:
            self.end()
            print("end")

    def action_frame(self):
        pass


class AnimOverlay(Animation):
    def __init__(self, frames, fadein: bool):
        if fadein:
            target = 0
        else:
            target = 256
        super().__init__(frames, target)
        self.delta_value = (target-config.alpha_overlay)/frames

    def action_frame(self):
        config.alpha_overlay = self.current_value
        self.current_value += self.delta_value
        self.check()
        print(self.current_value)
