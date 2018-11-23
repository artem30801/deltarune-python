from game_objects import *

game_state = "overworld"
current_game = None
current_room = None

camera_x = 0
camera_y = 0


def update_camera():
    x = current_game.playable.rect.centerx - WIDTH//2
    y = current_game.playable.rect.centery - WIDTH//2

    x = max(0, x)
    y = max(0, y)
    x = min((lvl_width-WIDTH), x)
    y = min((lvl_height-HEIGHT), y)

    return x, y


class Game:
    def __init__(self, player):
        self.offset_x = 0
        self.size_x = WIDTH
        self.size_y = HEIGHT

        self.playable = player

        self.active = True

    def player_control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.playable.control_speed(-self.playable.speed, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.playable.control_speed(self.playable.speed, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.playable.control_speed(0, -self.playable.speed)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                self.playable.control_speed(0, self.playable.speed)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.playable.control_speed(self.playable.speed, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.playable.control_speed(-self.playable.speed, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.playable.control_speed(0, self.playable.speed)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                self.playable.control_speed(0, -self.playable.speed)

    def resize(self, event):
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

            self.size_y = event.dict['size'][1]
            scale = self.size_y / HEIGHT
            self.size_x = int(scale * WIDTH)
            self.offset_x = (event.dict['size'][0] - self.size_x) // 2

    def dialog_control(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT or event.key == ord('x'):
                for dialog in dialog_list:  # TODO completely fix THAT SHIT
                    dialog.reset()
                global game_state
                game_state = "overworld"  # TODO fix that shit

    def render(self):

        # render all sprites
        camera_screen.blit(background, (0, 0))

        all_sprites.draw(camera_screen)
        fake_screen.blit(camera_screen, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))

        dialog_list.draw(fake_screen)

        # render fake screen
        screen.blit(pygame.transform.scale(fake_screen, (self.size_x, self.size_y)),
                    (self.offset_x, 0)

                    )

        pygame.display.update()

    def main_loop(self):
        while self.active:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.active = False

                self.resize(event)

                if game_state == "dialog":
                    self.dialog_control(event)

                if game_state == "overworld":
                    self.player_control(event)

                    for trigger in triggers_list:
                        trigger.check(event)

            obstacle_list.update()
            if game_state == "overworld":
                character_list.update()

            if game_state != "overworld":
                self.playable.stop()

            if game_state == "dialog":
                dialog_list.update()

            global camera_x, camera_y
            camera_x, camera_y = update_camera()
            self.render()

            time.tick(FPS)


class Trigger:
    def __init__(self):
        self.count = 0
        self.triggered = False

        triggers_list.append(self)

    def check(self, event):
        pass

    def action(self):
        pass


class InteractTrigger(Trigger):
    def __init__(self, target, result):
        super().__init__()
        self.target = target
        self.result = result

    def check(self, event):
        if not self.triggered:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == ord('z'):
                    if current_game.playable.vicinity_rect.colliderect(self.target):
                        self.action()

    def action(self):
        global game_state
        activate_dialog(self.result)


class StepOnTrigger(Trigger):  # TODO TODO
    def __init__(self, target, result):
        super().__init__()
        self.target = target
        self.result = result

    def check(self, event):
        if not self.triggered:
            if current_game.playable.footprint_rect.colliderect(self.target):
                self.action()

    def action(self):
        global game_state
        activate_dialog(self.result)


def activate_dialog(dialog):
    pygame.mixer.music.pause()
    dialog_list.add(dialog)
    global game_state
    game_state = "dialog"


def set_current_game(game):
    global current_game
    current_game = game


def set_current_room(room):
    global current_room
    current_room = room
