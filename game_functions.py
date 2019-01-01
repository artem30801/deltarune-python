from game_objects import *
config.game_state = "overworld"


class Window:
    def __init__(self):
        self.hwnd = None
        self.rect = None#pygame.Rect(0, 0, WIDTH, HEIGHT)

    def update(self):
        self.hwnd = pygame.display.get_wm_info()['window']
        self.rect = pygame.Rect(self.get_winrect())

    def get_winrect(self):
        prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
        paramflags = (1, "hwnd"), (2, "lprect")
        getrect = prototype(("GetWindowRect", windll.user32), paramflags)
        rect = getrect(self.hwnd)

        x = rect.left
        y = rect.top
        w = rect.right - rect.left
        h = rect.bottom - rect.top

        return x, y, w, h

    def set_position(self, x, y):
        w, h = self.rect.size
        windll.user32.MoveWindow(self.hwnd, x, y, w, h, False)

    def move(self, dx, dy, dw=0, dh=0):
        (x, y), (w, h) = self.rect.topleft, self.rect.size
        print(x, y, w, h)
        windll.user32.MoveWindow(self.hwnd, x+dx, y+dy, w+dw, h+dh, False)


window = Window()


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
        if Dialog.current_dialog is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT or event.key == ord('x'):
                    Dialog.current_dialog.skip()

                if event.key == pygame.K_RETURN or event.key == ord('z'):
                    Dialog.current_dialog.next()
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
        self.camera_x = min((Room.current_room.width - WIDTH), self.camera_x)
        self.camera_y = min((Room.current_room.height - HEIGHT), self.camera_y)

    def render(self):
        #render background
        Room.current_room.camera_screen.blit(Room.current_room.background, (0, 0))

        # render all sprites on whole room
        Room.current_room.background_sprites.draw(Room.current_room.camera_screen)
        Room.current_room.all_sprites.draw(Room.current_room.camera_screen)
        #Room.current_room.camera_screen.set_alpha(3)

        fake_screen.blit(Room.current_room.camera_screen, (0, 0), (self.camera_x, self.camera_y, WIDTH, HEIGHT))

        fake_screen.blit(alpha_surface, (0, 0))

        dialog_layer.draw(fake_screen)
        #fake_screen.set_alpha(20) пиздецовый сюр. мб пригодится

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
                    for trigger in Room.current_room.triggers_list:
                        trigger.check(event)

                elif config.game_state == "dialog":
                    self.dialog_control(event)

            window.update()

            for animation in active_animations:
                animation.action_frame()

            Room.current_room.background_sprites.update()
            if config.game_state == "overworld":
                Room.current_room.all_sprites.update()

            if config.game_state != "overworld":
                self.playable.stop()

            if config.game_state == "dialog":
                dialog_layer.update()

            self.update_camera()
            self.render()

            time.tick(FPS)
