import pygame
import json


class GameSetup:
    """
    This class is used to store screen parameters and functions
    """
    pygame.init()

    # Screen parameters:
    width = 0
    height = 0
    fps = 60
    screen = None

    # in-game icons
    hp_icon = None
    overheat_icon = None
    scrap_metal_icon = None
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

    # sounds
    button_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
    button_music = pygame.mixer.Sound("assets/sounds/background_music_volume.mp3")
    shooting_sound = pygame.mixer.Sound("assets/sounds/beam_shoot.mp3")  # Load sound file

    # low health blinking
    danger_blinking = settings["danger_blinking"]
    button_up = settings["button_up"]

    # vibrations
    vibrations = settings["vibrations"]
    vibration_time = 0
    vibration_start = 0

    #   buttons
    button_up = settings["button_up"]
    button_down = settings["button_down"]
    button_left = settings["button_left"]
    button_right = settings["button_right"]
    button_function_1 = settings["button_function_1"]
    button_function_2 = settings["button_function_2"]

    # joystick
    joysticks = None

    # languages
    all_languages = ['english', 'czech', 'french', 'german', 'spanish', 'cat']
    language = settings["language"]
    with open("languages.json", "r", encoding='utf-8') as languages_file:
        languages = json.load(languages_file)

    def __init__(self):
        # This is just there, so it can be a class :)
        pass

    @classmethod
    def set_language(cls, environment):
        for language in cls.languages:
            if language['language'] == cls.language:
                title = language['text'][environment]['title']
                game_text = language['text'][environment]['content']
                return title, game_text
    @classmethod
    def update(cls):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)

        #   sound
        cls.music_volume = settings["music_volume"]
        cls.effects_volume = settings["effects_volume"]

        # low health blinking
        cls.danger_blinking = settings["danger_blinking"]
        cls.vibrations = settings["vibrations"]
        cls.button_up = settings["button_up"]

        #   buttons
        cls.button_up = settings["button_up"]
        cls.button_down = settings["button_down"]
        cls.button_left = settings["button_left"]
        cls.button_right = settings["button_right"]
        cls.button_function_1 = settings["button_function_1"]
        cls.button_function_2 = settings["button_function_2"]


    @classmethod
    def start_setup(cls):
        """
        This function "sets the screen on". The object does not have to be created, it can be called anytime (but it
        really has to be called only at the beginning of the code). It also changes the window's name and loads the
        background image.
        """
        pygame.display.set_caption('Space shooter')
        # screen = pygame.display.set_mode((800, 600))  # Pavel_odkomentovávám pouze proto, abych viděl řádek
        cls.width, cls.height = 800,450
        screen = pygame.display.set_mode((cls.width, cls.height))
        cls.screen = screen
        cls.hp_icon = pygame.image.load("assets/icons/bars/health_bar.png")
        cls.hp_icon = pygame.transform.scale_by(cls.hp_icon, 2 / 1920 * cls.width)
        cls.hp_icon = pygame.Surface.convert_alpha(cls.hp_icon)
        cls.overheat_icon = pygame.image.load("assets/icons/bars/tempreture_bar.png")
        cls.overheat_icon = pygame.transform.scale_by(cls.overheat_icon, 2 / 1920 * cls.width)
        cls.overheat_icon = pygame.Surface.convert_alpha(cls.overheat_icon)
        cls.scrap_metal_icon = pygame.image.load('assets/images/scrap_metal0.png')
        cls.scrap_metal_icon = pygame.transform.scale(cls.scrap_metal_icon, (GameSetup.width / 1536 * 64,
                                                                             GameSetup.width / 1536 * 64))
        cls.scrap_metal_icon = pygame.Surface.convert_alpha(cls.scrap_metal_icon)
        return screen

    @classmethod
    def setup_controller(cls):
        cls.joysticks = []
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                cls.joysticks.append(joy)

        for joystick in cls.joysticks:
            joystick.init()

