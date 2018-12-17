from game_objects import *
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

user32 = windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

config.game_state = "overworld"


def get_winrect():
    hwnd = pygame.display.get_wm_info()['window']
    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")
    getrect = prototype(("GetWindowRect", windll.user32), paramflags)
    rect = getrect(hwnd)

    x = rect.left
    y = rect.top
    w = rect.right - rect.left
    h = rect.bottom - rect.top

    return x, y, w, h


def move_winrect(dx, dy, dw=0, dh=0):
    hwnd = pygame.display.get_wm_info()['window']
    x, y, w, h = get_winrect()
    windll.user32.MoveWindow(hwnd, x+dx, y+dy, w+dw, h+dh, False)


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
                self.playable.control_speed(-1, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.playable.control_speed(1, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.playable.control_speed(0, -1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                self.playable.control_speed(0, 1)
            if event.key == ord('x'):
                self.playable.speed = 10

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.playable.control_speed(1, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.playable.control_speed(-1, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.playable.control_speed(0, 1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                self.playable.control_speed(0, -1)
            if event.key == ord('x'):
                self.playable.speed = 5

    def resize(self, event):
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

            self.size_y = event.dict['size'][1]
            scale = self.size_y / HEIGHT
            self.size_x = int(scale * WIDTH)
            self.offset_x = (event.dict['size'][0] - self.size_x) // 2

    def dialog_control(self, event):
        if config.current_dialog is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT or event.key == ord('x'):
                    config.current_dialog.skip()
                if event.key == pygame.K_RETURN or event.key == ord('z'):
                    config.current_dialog.next()
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    pass
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    pass
                if event.key == pygame.K_UP or event.key == ord('w'):
                    pass
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    pass

    def update_camera(self):
        self.camera_x = self.playable.rect.centerx - WIDTH // 2
        self.camera_y = self.playable.rect.centery - HEIGHT // 2

        self.camera_x = max(0, self.camera_x)
        self.camera_y = max(0, self.camera_y)
        self.camera_x = min((config.current_room.width - WIDTH), self.camera_x)
        self.camera_y = min((config.current_room.height - HEIGHT), self.camera_y)

    def render(self):
        #render background
        config.current_room.camera_screen.blit(config.current_room.background, (0, 0))

        # render all sprites on whole room
        config.current_room.all_sprites.draw(config.current_room.camera_screen)

        fake_screen.blit(config.current_room.camera_screen, (0, 0), (self.camera_x, self.camera_y, WIDTH, HEIGHT))

        alpha_surface.set_alpha(config.alpha_overlay)
        fake_screen.blit(alpha_surface, (0, 0))

        dialog_layer.draw(fake_screen)

        # render fake screen
        screen.blit(pygame.transform.scale(fake_screen, (self.size_x, self.size_y)), (self.offset_x, 0))

        pygame.display.update()

    def main_loop(self):
        while self.active:
            pygame.event.post(pygame.event.Event(USEREVENT + 0, {}))  # fix to update triggers every frame
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.active = False

                self.resize(event)

                if config.game_state == "overworld":
                    self.player_control(event)
                    for trigger in config.current_room.triggers_list:
                        trigger.check(event)

                elif config.game_state == "dialog":
                    self.dialog_control(event)


            #config.current_room.obstacle_list.update()
            if config.game_state == "overworld":
                config.current_room.all_sprites.update()
                #config.current_room.character_list.update()

            if config.game_state != "overworld":
                self.playable.stop()

            if config.game_state == "dialog":
                dialog_layer.update()

            for animation in active_animations:
                animation.action_frame()

            self.update_camera()
            self.render()
            move_winrect(0, 0)

            time.tick(FPS)
