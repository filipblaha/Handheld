import pygame
import json
from gamesetup import GameSetup


class Button:
    def __init__(self, x_button, y_button, image_01_path, image_02_path, scale_w, scale_h, text_size, text, screen_in_button, sound, sound_volume, joystick, joystick_index=None):
        self.scale_w = scale_w
        self.scale_h = scale_h
        self.x_button = x_button
        self.y_button = y_button
        self.width_screen = screen_in_button.get_width()    # getting screen width
        self.clicked = False    # the button is not clicked at the beginning
        self.collision = False  # at the beginning, no collision occurs
        self.press = False      # the button cannot be pressed at the beginning
        self.mask_01_collision = False  # the is not anz collision with mouse and first mask at the beginning
        self.joystick = joystick
        self.joystick_index = joystick_index

        # image_01
        self.image_01 = pygame.image.load(image_01_path).convert_alpha()  # load button image with transparency

        # image_02
        self.image_02 = pygame.image.load(image_02_path).convert_alpha()  # load button image with transparency

        # text
        font_size = text_size * self.width_screen
        self.font = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size))  # loading font
        self.font_parameters = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size*0.5))  # loading font for ship parameters
        self.text_to_write = text

        # sound
        self.sound_volume = sound_volume
        self.sound = sound  # Load sound file
        self.sound.set_volume(self.sound_volume * GameSetup.effects_volume)

        #   ship parameters
        # load information about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)

        # selection of ship
        if image_01_path == "assets/images/player_light/vlod_player_light.png":
            self.Ship_param = player_param[0]
        elif image_01_path == "assets/images/player_mid/vlod_player_mid.png":
            self.Ship_param = player_param[1]
        else:
            self.Ship_param = player_param[2]

    def update_text(self, text):
        self.text_to_write = text

    def draw_image_topRight(self, surface):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
        #   button
        # button_01
        image_01 = pygame.transform.scale(self.image_01, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_01
        rect_01 = image_01.get_rect()  # creates a rectangular frame around the object's image_01
        rect_01.topright = (self.x_button, self.y_button)  # placing topright corner of image_01 to wanted position
        image_01_mask = pygame.mask.from_surface(image_01)  # mask from image_01
        # button_02
        image_02 = pygame.transform.scale(self.image_02, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_02
        rect_02 = image_02.get_rect()  # creates a rectangular frame around the object's image_02
        rect_02.topright = (self.x_button, self.y_button)  # placing topright corner of image_02 to wanted position
        image_02_mask = pygame.mask.from_surface(image_02)  # mask from image_02
        # selecting an image for interaction and display on the screen
        if not self.collision:  # image_01 is used for interaction and is displayed on screen
            surface.blit(image_01, rect_01)
            rect = rect_01
            mask = image_01_mask
        else:
            surface.blit(image_02, rect_02)  # image_02 is used for interaction and is displayed on screen
            rect = rect_02
            mask = image_02_mask
        # collision check
        if rect.collidepoint(mouse_x, mouse_y):
            offset_x = mouse_x - rect.x
            offset_y = mouse_y - rect.y
            if mask.get_at((offset_x, offset_y)):
                self.collision = True
                if pygame.mouse.get_pressed()[0] == 0:  # this makes it impossible to click outside the button and then hover over it and activate it without clicking
                    self.press = True
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.press == 1:
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False
                    self.sound.set_volume(self.sound_volume * GameSetup.effects_volume)
                    pygame.mixer.Channel(1).play(self.sound)
                    action = True
            else:
                self.collision = False
                self.clicked = False
                self.press = False
        else:
            self.collision = False
            self.clicked = False
            self.press = False

        return action

    def draw_image_in_center(self, surface, game_text):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
        #   button
        # button_01
        image_01 = pygame.transform.scale(self.image_01, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_01
        rect_01 = image_01.get_rect()  # creates a rectangular frame around the object's image_01
        rect_01.center = (self.x_button, self.y_button)  # placing center of image_01 to wanted position
        image_01_mask = pygame.mask.from_surface(image_01)  # mask from image_01
        # button_02
        image_02 = pygame.transform.scale(self.image_02, (int(self.width_screen * self.scale_w * 1.3), int(self.width_screen * self.scale_h * 1.3)))  # transforming image_02
        rect_02 = image_02.get_rect()  # creates a rectangular frame around the object's image_02
        rect_02.center = (self.x_button, self.y_button)  # placing center of image_02 to wanted position
        image_02_mask = pygame.mask.from_surface(image_02)  # mask from image_02
        #   selecting an image for interaction and display on the screen
        if not self.collision:  # image_01 is used for interaction and is displayed on screen
            surface.blit(image_01, rect_01)
            rect = rect_01
            mask = image_01_mask
            text_color = (150, 150, 150)
        else:
            surface.blit(image_02, rect_02) # image_02 is used for interaction and is displayed on screen
            rect = rect_02
            mask = image_02_mask
            text_color = (230, 230, 230)

        # selecting an image for interaction and display on the screen
        if self.joystick.active:
            # position check
            if self.joystick.position == self.joystick_index:
                self.collision = True
            else:
                self.collision = False

        else:
            # when this "if" is not there, there is a flicker between image_01 and image_02 on the interface
            if rect_01.collidepoint(mouse_x, mouse_y):
                offset_x_01 = mouse_x - rect_01.x
                offset_y_01 = mouse_y - rect_01.y
                if image_01_mask.get_at((offset_x_01, offset_y_01)):
                    self.mask_01_collision = True
                else:
                    self.mask_01_collision = False
            else:
                self.mask_01_collision = False

            # main collision check and action
            if rect.collidepoint(mouse_x, mouse_y):
                offset_x = mouse_x - rect.x
                offset_y = mouse_y - rect.y
                if mask.get_at((offset_x, offset_y)) or self.mask_01_collision == True:
                    self.collision = True
                    if pygame.mouse.get_pressed()[0] == 0:  # this makes it impossible to click outside the button and then hover over it and activate it without clicking
                        self.press = True
                    if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.press == 1:
                        self.clicked = True
                    if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                        self.clicked = False
                        self.sound.set_volume(self.sound_volume * GameSetup.effects_volume)
                        pygame.mixer.Channel(1).play(self.sound)
                        action = True
                else:
                    self.collision = False
                    self.clicked = False
                    self.press = False
            else:
                self.collision = False
                self.clicked = False
                self.press = False
        #   text
        text = self.font.render(self.text_to_write, True, text_color)
        text_rect = text.get_rect()
        text_rect.centerx = self.x_button
        text_rect.centery = self.y_button - (rect_02.height/2) * 1.3
        # draw text on screen
        surface.blit(text, text_rect)
        #   Printing ship parameters
        if self.Ship_param['type'] == 'player_light':
            q_skill = game_text[7]
            e_skill = game_text[8]

        if self.Ship_param['type'] == 'player_mid':
            q_skill = game_text[9]
            e_skill = game_text[10]

        if self.Ship_param['type'] == 'player_tank':
            q_skill = game_text[11]
            e_skill = game_text[12]
        ship_text = [f"{game_text[0]}{self.Ship_param['hp'][0]}", f"{game_text[1]}{self.Ship_param['proj_dmg'][0]}", f"{game_text[2]}{self.Ship_param['fire_rate'][0]}", f"{game_text[3]}{self.Ship_param['acceleration'][0]}", f"{game_text[4]}{self.Ship_param['max_velocity']}", game_text[5] + q_skill, game_text[6] + e_skill]
        y_position = [self.y_button + (rect_02.height/2) * 1.3, self.y_button + (rect_02.height/2) * 1.6, self.y_button + (rect_02.height/2) * 1.9, self.y_button + (rect_02.height/2) * 2.2, self.y_button + (rect_02.height/2) * 2.5, self.y_button + (rect_02.height/2) * 3, self.y_button + (rect_02.height/2) * 3.3]
        for parameters, position in zip(ship_text, y_position):
            text = self.font_parameters.render(str(parameters), True, text_color)
            text_rect = text.get_rect()
            text_rect.centerx = self.x_button
            text_rect.centery = position
            # draw text on screen
            surface.blit(text, text_rect)

        return action

    def draw_button_and_text(self, surface, center=False, always_on=False):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position

        #   button
        # button_01
        image_01 = pygame.transform.scale(self.image_01, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_01
        rect_01 = image_01.get_rect()  # creates a rectangular frame around the object's image_01
        rect_01.topleft = (self.x_button, self.y_button)  # placing topleft corner of image_01 to wanted position
        image_01_mask = pygame.mask.from_surface(image_01)  # mask from image_01

        # button_02
        image_02 = pygame.transform.scale(self.image_02, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_02
        rect_02 = image_02.get_rect()  # creates a rectangular frame around the object's image_02
        rect_02.topleft = (self.x_button, self.y_button)  # placing topleft corner of image_02 to wanted position
        image_02_mask = pygame.mask.from_surface(image_02)  # mask from image_02

        if self.collision:
            surface.blit(image_02, rect_02)   # image_02 is used for interaction and is displayed on screen
            rect = rect_02
            mask = image_02_mask
            text_color = (0, 0, 0)
        else:
            surface.blit(image_01, rect_01)   # image_01 is used for interaction and is displayed on screen
            rect = rect_01
            mask = image_01_mask
            text_color = (40, 40, 40)

        # selecting an image for interaction and display on the screen
        if self.joystick.active:
            # position check
            if self.joystick.position == self.joystick_index and not always_on:
                self.collision = True
            else:
                self.collision = False

        else:
            # collision check
            if rect.collidepoint(mouse_x, mouse_y):
                offset_x = mouse_x - rect.x
                offset_y = mouse_y - rect.y
                if mask.get_at((offset_x, offset_y)):
                    self.collision = True
                    if pygame.mouse.get_pressed()[0] == 0:  # this makes it impossible to click outside the button and then hover over it and activate it without clicking
                        self.press = True
                    if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.press == 1:
                        self.clicked = True
                    if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                        self.clicked = False
                        self.sound.set_volume(self.sound_volume * GameSetup.effects_volume)
                        pygame.mixer.Channel(1).play(self.sound)
                        action = True
                else:
                    self.collision = False
                    self.clicked = False
                    self.press = False
            else:
                self.collision = False
                self.clicked = False
                self.press = False
        #   text
        text = self.font.render(self.text_to_write, True, text_color)
        text_rect = text.get_rect()
        image_height = rect.height  # height of image
        text_height = text.get_height()  # height of text

        if center:
            text_rect.center = rect_01.center
        else:
            text_rect.x = self.x_button + (text_height / 2)
            text_rect.y = self.y_button - (text_height / 2) + (image_height / 2)

        # draw text on screen
        surface.blit(text, text_rect)

        return action
