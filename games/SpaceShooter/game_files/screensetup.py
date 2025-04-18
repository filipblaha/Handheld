import pygame
import json


class ScreenSetup:
    """
    This class is used to store screen parameters and functions
    """
    pygame.init()

    # Screen parameters:
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    fps = 60
    screen = None

    # in-game icons
    hp_icon = None
    overheat_icon = None
    q_action_icon_off = None
    q_action_icon_on = None
    e_action_icon_off = None
    e_action_icon_on = None

    # reading settings
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    #   sound
    music_volume = settings["music_volume"]
    effects_volume = settings["effects_volume"]
    #   buttons
    button_up = settings["button_up"]
    button_down = settings["button_down"]
    button_left = settings["button_left"]
    button_right = settings["button_right"]
    button_function_1 = settings["button_function_1"]
    button_function_2 = settings["button_function_2"]

    def __init__(self):
        # This is just there, so it can be a class :)
        pass

    @classmethod
    def start_setup(cls):
        """
        This function "sets the screen on". The object does not have to be created, it can be called anytime (but it
        really has to be called only at the beginning of the code). It also changes the window's name and loads the
        background image.
        """
        pygame.display.set_caption('Space shooter')
        screen = pygame.display.set_mode((cls.width, cls.height), pygame.FULLSCREEN)
        cls.width, cls.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        cls.screen = screen
        cls.hp_icon = pygame.image.load("assets/icons/bars/health_bar.png")
        cls.hp_icon = pygame.transform.scale_by(cls.hp_icon, 2 / 1920 * cls.width)
        cls.hp_icon = pygame.Surface.convert_alpha(cls.hp_icon)
        cls.overheat_icon = pygame.image.load("assets/icons/bars/tempreture_bar.png")
        cls.overheat_icon = pygame.transform.scale_by(cls.overheat_icon, 2 / 1920 * cls.width)
        cls.overheat_icon = pygame.Surface.convert_alpha(cls.overheat_icon)
        return screen
