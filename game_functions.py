from game_objects import *

config.game_state = "overworld"
current_game = None


def update_camera():
    x = current_game.playable.rect.centerx - WIDTH//2
    y = current_game.playable.rect.centery - WIDTH//2

    x = max(0, x)
    y = max(0, y)
    x = min((config.current_room.width-WIDTH), x)
    y = min((config.current_room.height-HEIGHT), y)

    return x, y


class Game:
    def __init__(self, player):
        self.offset_x = 0
        self.size_x = WIDTH
        self.size_y = HEIGHT

        self.camera_x = 0
        self.camera_y = 0

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
                config.game_state = "overworld"  # TODO fix that shit

    def render(self):
        # render all sprites
        config.current_room.camera_screen.blit(config.current_room.background, (0, 0))

        config.current_room.all_sprites.draw(config.current_room.camera_screen)
        fake_screen.blit(config.current_room.camera_screen, (0, 0), (self.camera_x, self.camera_y, WIDTH, HEIGHT))

        dialog_list.draw(fake_screen)

        # render fake screen
        screen.blit(pygame.transform.scale(fake_screen, (self.size_x, self.size_y)), (self.offset_x, 0))
        pygame.display.update()

    def main_loop(self):
        while self.active:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.active = False

                self.resize(event)

                if config.game_state == "dialog":
                    self.dialog_control(event)

                if config.game_state == "overworld":
                    self.player_control(event)

                    for trigger in triggers_list:
                        trigger.check(event)

            config.current_room.obstacle_list.update()
            if config.game_state == "overworld":
                config.current_room.character_list.update()

            if config.game_state != "overworld":
                self.playable.stop()

            if config.game_state == "dialog":
                dialog_list.update()

            self.camera_x, self.camera_y = update_camera()
            self.render()

            time.tick(FPS)


class Trigger:
    def __init__(self, result, once=False):
        self.count = 0
        self.triggered = False
        self.once = once

        self.result = result

        triggers_list.append(self)

    def check(self, event):
        pass

    def action(self):
        self.result.activate()

        if self.once:
            triggers_list.remove(self)


class InteractTrigger(Trigger):
    def __init__(self, result, target):
        super().__init__(result)
        self.target = target

    def check(self, event):
        if not self.triggered:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == ord('z'):
                    if current_game.playable.vicinity_rect.colliderect(self.target):
                        self.action()


def set_current_game(game):
    global current_game
    current_game = game
