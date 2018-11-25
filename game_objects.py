from game_init import *
import config


dialog_list = pygame.sprite.Group()


class Room:
    def __init__(self, width, height, music_name=None):
        self.width = width
        self.height = height
        self.music = music_name

        self.triggers_list = []

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacle_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()
        # TODO list of dialogs

        self.camera_screen = pygame.Surface((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))

    def generate_floor(self, tiles, type_name, back_color=(0, 0, 0)):
        self.background.fill(back_color)
        images = []
        for i in range(0, 26 + 1):
            img = pygame.image.load(os.path.join('images', 'env', 'tiles', type_name, 'tile' + str(i).zfill(3) + '.png')).convert()
            img = pygame.transform.scale2x(img)
            img.convert_alpha()
            # img.set_colorkey(ALPHA)
            images.append(img)

        for y, row in enumerate(tiles):
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

        pygame.mixer.music.stop()
        if self.music is not None:
            pygame.mixer.music.load(os.path.join('music', self.music + '.mp3'))
            pygame.mixer.music.play(-1)


class RoomPortal:
    def __init__(self, room1, room2, tp_position=(0, 0), sound_name=None):
        self.room1 = room1
        self.room2 = room2

        self.tp_position = tp_position

        self.sound = None
        if sound_name is not None:
            self.sound = pygame.mixer.Sound(os.path.join('SFX', sound_name + '.wav'))

    def activate(self):
        config.current_game.playable.rect.topleft = self.tp_position
        if self.sound is not None:
            self.sound.play()
        if config.current_room == self.room1:
            self.room2.activate()


class RoomPortalStep(RoomPortal):
    def __init__(self, room1, room2, tp_position=(0, 0), position=(0, 0, 80, 80), sound_name=None):
        super().__init__(room1, room2, tp_position, sound_name)
        self.position = position
        portal = GameObj(None, None, position=(position[0], position[1]))
        trigger = StepOnTrigger(self, portal)
        room1.bind(portal)
        room1.bind_triggers(trigger)


class GameObj(pygame.sprite.Sprite):
    def __init__(self, img_class, img_name, animation_cycle=1, sprite_count=1, speed=5,
                 position=(0, 0), empty_size=(80, 85)):
        pygame.sprite.Sprite.__init__(self)

        self.movex = 0
        self.movey = 0
        self.position = position

        self.speed = speed

        self.frame = 0
        self.animation_cycle = animation_cycle
        self.sprite_count = sprite_count

        self.images = []
        for i in range(1, self.sprite_count + 1):
            if img_name is not None:
                img = pygame.image.load(os.path.join('images', img_class, img_name + str(i) + '.png')).convert()
                img.set_colorkey(ALPHA)
                img.convert_alpha()
                img = pygame.transform.scale2x(img)
            else:
                img = pygame.Surface(empty_size)
                img.set_colorkey(ALPHA)

            # img = pygame.transform.smoothscale(img, (scale*img.get_width(), scale*img.get_height()))
            self.images.append(img)

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


class Chara(GameObj):
    def __init__(self, img_name):
        super().__init__('characters', img_name, 3, 16)

        self.boundary = (0, 70, 40, 15)

        self.footprint_rect = pygame.rect.Rect((self.boundary[0] + self.rect.x,
                                                self.boundary[1] + self.rect.y,
                                                self.boundary[2], self.boundary[3]
                                                ))

        self.vicinity_rect = self.rect.inflate(10, 10)
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
                    collide_y = True
        # collide with room border
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
    def __init__(self, img_name, position=(0, 0), boundary=(0, 0, 80, 80), animation_cycle=1, sprite_count=1,):
        super().__init__('env', img_name, animation_cycle, sprite_count, position=position)

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


class Dialog:
    def __init__(self, *speech):
        self.speeches = speech
        self.count = len(self.speeches)
        self.current = 0

    def next(self):
        self.current += 1

    def end(self):
        pass


class Speech(pygame.sprite.Sprite):
    def __init__(self, text, font, img_name, sound_name, speed=3):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont(font, 72)
        self.size = 150
        self.frame = 0
        self.speed = speed

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

    def activate(self):
        pygame.mixer.music.pause()
        dialog_list.add(self)
        config.game_state = "dialog"

    def reset(self):
        dialog_list.remove(self)
        self.frame = 0
        pygame.mixer.music.unpause()


class DialogChoice:  #TODO
    pass


class Trigger:
    def __init__(self, result, once=False):
        self.count = 0
        self.triggered = False
        self.once = once

        self.result = result

    def check(self, event):
        pass

    def action(self):
        if self.once:
            config.current_room.triggers_list.remove(self)
        self.result.activate()


class InteractTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if not self.triggered:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == ord('z'):
                    if config.current_game.playable.vicinity_rect.colliderect(self.target.footprint_rect):
                        self.action()


class StepOnTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if not self.triggered:
            if config.current_game.playable.footprint_rect.colliderect(self.target.rect):
                self.action()
