from game_init import *
import config


dialog_list = pygame.sprite.Group()

triggers_list = []


class Room:
    def __init__(self, width, height, music_name=None):
        self.width = width
        self.height = height
        self.music = music_name

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacle_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()
        # TODO list of dialogs

        self.camera_screen = pygame.Surface((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((100, 100, 100))  # TODO background generator

    def bind(self, *game_objects):
        for obj in game_objects:
            self.all_sprites.add(obj)
            if isinstance(obj, Obstacle):
                self.obstacle_list.add(obj)
            if isinstance(obj, Chara):
                self.character_list.add(obj)

    def activate(self):
        config.current_room = self

        pygame.mixer.music.stop()
        if self.music is not None:
            pygame.mixer.music.load(os.path.join('music', self.music + '.mp3'))
            pygame.mixer.music.play()


class RoomPortal:
    def __init__(self, room1, room2):
        self.room1 = room1
        self.room2 = room2

    def activate(self):
        if config.current_room == self.room1:
            self.room2.activate()


class GameObj(pygame.sprite.Sprite):
    def __init__(self, img_class, img_name, animation_cycle=1, sprite_count=1, speed=5,
                 boundary=(0, 0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.movex = 0
        self.movey = 0
        self.boundary = boundary

        self.speed = speed

        self.frame = 0
        self.animation_cycle = animation_cycle
        self.sprite_count = sprite_count

        self.images = []
        for i in range(1, self.sprite_count + 1):
            img = pygame.image.load(os.path.join('images', img_class, img_name + str(i) + '.png')).convert()
            img = pygame.transform.scale2x(img)
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.footprint_rect = pygame.rect.Rect((self.boundary[0]+self.rect.x,
                                                self.boundary[1]+self.rect.y,
                                                self.boundary[2], self.boundary[3]
                                                ))

        self._layer = self.rect.bottom

        #current_room.all_sprites.add(self)

    def control_speed(self, x, y):
        self.movex += x
        self.movey += y

    def stop(self):
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        self.frame += 1
        if self.frame > self.animation_cycle:
            self.frame = 0
        frame_offset = -1

        self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]

        self.footprint_rect.x = self.rect.x + self.boundary[0]
        self.footprint_rect.y = self.rect.y + self.boundary[1]
        config.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Chara(GameObj):
    def __init__(self, img_name):
        super().__init__('characters', img_name, 4, 16, boundary=(0, 75, 25, 5))

        self.vicinity_rect = self.rect.inflate(10, 10)
        self.vicinity_rect.center = self.rect.center

        #character_list.add(self)

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        self.footprint_rect.midbottom = self.rect.midbottom

        if self.movey > 0:
            self.frame += 1
            if self.frame > 3 * self.animation_cycle:
                self.frame = 0
            frame_offset = 0
            self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]

        if self.movey < 0:
            self.frame += 1
            if self.frame > 3 * self.animation_cycle:
                self.frame = 0
            frame_offset = 12
            self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]

        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * self.animation_cycle:
                self.frame = 0
            frame_offset = 4
            self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]

        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * self.animation_cycle:
                self.frame = 0
            frame_offset = 8
            self.image = self.images[(self.frame // self.animation_cycle) + frame_offset]

        for obstacle in config.current_room.obstacle_list:
            # collide = pygame.sprite.collide_mask(self, obstacle)
            if self.footprint_rect.colliderect(obstacle.footprint_rect):
                if self.movex != 0:
                    self.rect.x = self.rect.x - self.movex
                if self.movey != 0:
                    self.rect.y = self.rect.y - self.movey

        # collide with room border
        if self.rect.x < 0 or self.rect.right > config.current_room.width:
            self.rect.x = self.rect.x - self.movex
        if self.rect.y < 0 or self.rect.bottom > config.current_room.height:
            self.rect.y = self.rect.y - self.movey

        self.vicinity_rect.center = self.rect.center

        config.current_room.all_sprites.change_layer(self, self.rect.bottom)


class Obstacle(GameObj):
    def __init__(self, x, y, img_name, frames=1, boundary=(0, 0, 100, 100)):
        super().__init__('env', img_name, frames, boundary=boundary)

        self.rect.x = x
        self.rect.y = y

        #self.update()

        #obstacle_list.add(self)


class Speech(pygame.sprite.Sprite):
    def __init__(self, text, font, img_name, sound_name, speed, img_size=150):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont(font, 72)
        self.size = img_size
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


class Dialog:
    def __init__(self, *speech):
        self.speeches = speech
        self.count = len(self.speeches)
        self.current = 0

    def next(self):
        self.current += 1

    def end(self):
        pass
