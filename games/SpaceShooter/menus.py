import pygame
import button
from renderupdate import *
from leaderboard import *
import datetime
import drawText
from slider import Slider
from ship_upgrade import *
from collisions import *

from enemy_spawn import EnemySpawner
from playerships.mini_player import *
from background import Background
from itemspawn import ItemSpawner
from cursor import Cursor


def settings_menu(screen, joystick, cursor, clock, cursor_group, background, environment):
    width, height = screen.get_size()
    joystick.set_position(1, 0)
    #   fonts
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    font_subTitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))  # loading font
    font_height = font_subTitle.get_height()

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent

    # background
    # fill the whole screen with black transparent color

    background_cat = pygame.image.load(f"assets/images/background_cat.png").convert_alpha()
    background_cat = pygame.transform.scale(background_cat, (width, height))
    cat_rect = pygame.rect.Rect(0.955 * width, 0.75 * height, 20, 20)
    if environment == "main":
        surface.fill((0, 0, 0, 80))
    else:
        surface.fill((0, 0, 0, 170))

        # languages
    # flags
    flags = ['eng', 'cz', 'fr', 'de', 'esp']
    flag_rects = []
    flags_images = []
    flag_width = 0
    flag_height = 0
    on_language = False
    flag_offset_x = width / 44
    flag_offset_y = height / 29
    for i, flag in enumerate(flags):
        flag_surf = pygame.image.load(f"assets/images/languages/{flag}.png").convert_alpha()
        flag_width = int(flag_surf.get_width() * 0.0004 * width)
        flag_height = int(flag_surf.get_height() * 0.0004 * width)
        flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
        flag_rect = pygame.rect.Rect(0.93 * width, 0.03 * height + (flag_offset_y / 2 + flag_height) * i, flag_width,
                                     flag_height)
        flags_images.append(flag_surf)
        flag_rects.append(flag_rect)

    # flags background
    background_flag_width = flag_width + flag_offset_x
    background_flag_height = len(flags_images) * (flag_offset_y / 2 + flag_height) + flag_offset_y / 2
    flag_background = pygame.Surface((int(background_flag_width), int(background_flag_height)))
    flag_background.set_alpha(50)
    flag_background.fill('gray')
    flag_background_rect = flag_background.get_rect()
    flag_background_rect.x = 0.93 * width - flag_offset_x / 2
    flag_background_rect.y = 0.03 * height - flag_offset_y / 2

    #   volume
    min_value = 0
    max_value = 10
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    music_volume = settings["music_volume"]
    effects_volume = settings["effects_volume"]
    danger_blinking = settings["danger_blinking"]
    vibrations = settings["vibrations"]

    # text
    title, game_text = GameSetup.set_language("settings")

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    buttons_num = 6
    danger_button_on = button.Button(width / 6, height / 1.53, "assets/images/switch_on0.png",
                                     "assets/images/switch_on1.png", 0.1, 0.05, 0.025, '', screen,
                                     sound, sound_volume, joystick, (0, 3))
    danger_button_off = button.Button(width / 6, height / 1.53, "assets/images/switch_off0.png",
                                      "assets/images/switch_off1.png", 0.1, 0.05, 0.025, '', screen,
                                      sound, sound_volume, joystick, (0, 3))
    vibrations_button_on = button.Button(width / 6, height / 1.23, "assets/images/switch_on0.png",
                                         "assets/images/switch_on1.png", 0.1, 0.05, 0.025, '', screen,
                                         sound, sound_volume, joystick, (0, 4))
    vibrations_button_off = button.Button(width / 6, height / 1.23, "assets/images/switch_off0.png",
                                          "assets/images/switch_off1.png", 0.1, 0.05, 0.025, '', screen,
                                          sound, sound_volume, joystick, (0, 4))
    back_button = button.Button(0.8 * width, 7 / 8 * height, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.18, 0.05, 0.025, game_text[3], screen,
                                sound, sound_volume, joystick, (0, 5))

    # percentage
    percentageMusic = ((music_volume - min_value) / (max_value - min_value)) * 100
    percentageEffects = ((effects_volume - min_value) / (max_value - min_value)) * 100
    #   sliders
    sliderMusic = Slider((3.6 * width / 20), (27 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015),
                         min_value, max_value, percentageMusic, joystick, 1)
    sliderEffects = Slider((3.6 * width / 20), (37 * height / 80 + font_height * 2), (width * 0.375), (width * 0.015),
                           min_value, max_value, percentageEffects, joystick, 2)
    while True:
        mouse_pressed = False
        mouse_pos = pygame.mouse.get_pos()

        # background
        # easter cat
        if GameSetup.language == 'czech' or GameSetup.language == 'cat':
            screen.blit(background_cat, (0, 0))
        else:
            screen.blit(background, (0, 0))

        screen.blit(surface, (0, 0))

        # button update
        back_button.update_text(game_text[4])

        # render languages
        if on_language:
            screen.blit(flag_background, flag_background_rect)
            for i, rect in enumerate(flag_rects):
                if rect.collidepoint(mouse_pos):
                    flag_surf = flags_images[i]
                    flag_width = int(flag_surf.get_width() * 1.3)
                    flag_height = int(flag_surf.get_height() * 1.3)
                    flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
                    flag_rect = flag_surf.get_rect()
                    flag_rect.center = rect.center
                    screen.blit(flag_surf, flag_rect)
                else:
                    screen.blit(flags_images[i], flag_rects[i])
        else:
            if GameSetup.language == 'cat':
                language_index = GameSetup.all_languages.index('czech')
            else:
                language_index = GameSetup.all_languages.index(GameSetup.language)
            if flag_rects[0].collidepoint(mouse_pos):
                flag_surf = flags_images[language_index]
                flag_width = int(flag_surf.get_width() * 1.3)
                flag_height = int(flag_surf.get_height() * 1.3)
                flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
                flag_rect = flag_surf.get_rect()
                flag_rect.center = flag_rects[0].center
                screen.blit(flag_surf, flag_rect)
            else:
                screen.blit(flags_images[language_index], flag_rects[0])

        # text "Settings"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))

        # changing volume
        screen.blit(font_subTitle.render(game_text[0], True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_subTitle.render(game_text[1], True, (230, 230, 230)), (3.6 * width / 20, 37 * height / 80))

        # danger blinking
        screen.blit(font_subTitle.render(game_text[2], True, (230, 230, 230)),
                    (3.6 * width / 20, 52 * height / 87))

        # vibrations
        screen.blit(font_subTitle.render(game_text[3], True, (230, 230, 230)),
                    (3.6 * width / 20, 52 * height / 68))



        #   BUTTON
        if back_button.draw_button_and_text(screen, True, on_language):
            pygame.mixer.Channel(3).stop()
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                pygame.mixer.Channel(3).stop()
                return
            elif event.type == pygame.MOUSEBUTTONUP and not mouse_pressed:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # easter cat
                if cat_rect.collidepoint(mouse_pos):
                    GameSetup.language = 'cat'
                    on_language = False
                    title, game_text = GameSetup.set_language("settings")
                    settings["language"] = GameSetup.language
                    with open("settings.json", "w") as settings_file:
                        json.dump(settings, settings_file, indent=4)
                # switching danger blinking
                mouse_pressed = False
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

                # clicking on languages
                if on_language:
                    for i, rect in enumerate(flag_rects):
                        if rect.collidepoint(mouse_pos):
                            GameSetup.language = GameSetup.all_languages[i]
                            on_language = False
                            title, game_text = GameSetup.set_language("settings")
                            settings["language"] = GameSetup.language
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                elif flag_rects[0].collidepoint(mouse_pos):
                    if on_language:
                        on_language = False
                    else:
                        on_language = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                pygame.mixer.Channel(3).stop()
                return

            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        if danger_blinking:
            if danger_button_on.draw_button_and_text(screen, False, on_language):
                settings["danger_blinking"] = False
                danger_blinking = False
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()
        else:
            if danger_button_off.draw_button_and_text(screen, False, on_language):
                settings["danger_blinking"] = True
                danger_blinking = True
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

        if vibrations:
            if vibrations_button_on.draw_button_and_text(screen, False, on_language):
                settings["vibrations"] = False
                vibrations = False
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()
        else:
            if vibrations_button_off.draw_button_and_text(screen, False, on_language):
                settings["vibrations"] = True
                vibrations = True
                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

        #   volume
        # music
        sliderMusic.draw(screen, on_language)
        sliderMusic.update(settings, "music_volume", on_language)

        # effects
        sliderEffects.draw(screen, on_language)
        sliderEffects.update(settings, "effects_volume", on_language)

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False
            action = joystick.menu_control(1, buttons_num)
            if on_language:
                flag_surf = flags_images[joystick.position[1]]
                flag_width = int(flag_surf.get_width() * 1.3)
                flag_height = int(flag_surf.get_height() * 1.3)
                flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
                flag_rect = flag_surf.get_rect()
                flag_rect.center = flag_rects[joystick.position[1]].center
                screen.blit(flag_surf, flag_rect)

                if action == 'enter':
                    GameSetup.language = GameSetup.all_languages[joystick.position[1]]
                    title, game_text = GameSetup.set_language("settings")
                    settings["language"] = GameSetup.language
                    with open("settings.json", "w") as settings_file:
                        json.dump(settings, settings_file, indent=4)
                    on_language = False

                    joystick.set_position(0, 0)

                elif action == 'exit':
                    on_language = False
            else:
                if joystick.position[1] == 0:
                    language_index = GameSetup.all_languages.index(GameSetup.language)
                    flag_surf = flags_images[language_index]
                    flag_width = int(flag_surf.get_width() * 1.3)
                    flag_height = int(flag_surf.get_height() * 1.3)
                    flag_surf = pygame.transform.scale(flag_surf, (flag_width, flag_height))
                    flag_rect = flag_surf.get_rect()
                    flag_rect.center = flag_rects[0].center
                    screen.blit(flag_surf, flag_rect)
                if action == 'enter':
                    if joystick.position[1] == 0:
                        on_language = True
                    elif joystick.position[1] == 3:
                        if danger_blinking:
                            settings["danger_blinking"] = False
                            danger_blinking = False
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                            GameSetup.update()
                        else:
                            settings["danger_blinking"] = True
                            danger_blinking = True
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                            GameSetup.update()

                    elif joystick.position[1] == 4:
                        if vibrations:
                            settings["vibrations"] = False
                            vibrations = False
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                            GameSetup.update()
                        else:
                            GameSetup.joysticks[0].rumble(1, 1, 300)
                            settings["vibrations"] = True
                            vibrations = True
                            with open("settings.json", "w") as settings_file:
                                json.dump(settings, settings_file, indent=4)
                            GameSetup.update()
                    elif joystick.position[1] == 5:
                        pygame.mixer.Channel(3).stop()
                        sound.set_volume(sound_volume * GameSetup.effects_volume)
                        pygame.mixer.Channel(1).play(sound)
                        return

                elif action == 'exit':
                    pygame.mixer.Channel(3).stop()
                    sound.set_volume(sound_volume * GameSetup.effects_volume)
                    pygame.mixer.Channel(1).play(sound)

                    return
        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def save_name_menu(screen, joystick, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_info = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    #   create button instances
    save_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Save', screen,
                                "assets/sounds/button_click.mp3", 0.2)
    cancel_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                  "assets/images/button_02.png", 0.3, 0.05, 0.025, 'Cancel', screen,
                                  "assets/sounds/button_click.mp3", 0.2)
    #   the current date
    date = f'{datetime.datetime.now().date()}'
    #   name input
    user_name = ''
    font_input = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))
    text_box = pygame.Rect(3.6 * width / 20, 28 * height / 80, width / 2.5, width / 20)
    #   selected ship from nuber
    if ship_number == 1:
        selected_ship = "Light"
    elif ship_number == 2:
        selected_ship = "Mid"
    else:
        selected_ship = "Tank"
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Your name"
        screen.blit(font_title.render("Your name", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   button
        # if there is some input text
        if len(user_name) > 0:
            if save_button.draw_button_and_text(screen):
                save(highscore)
                return True
        if cancel_button.draw_button_and_text(screen):
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return False
            if event.type == pygame.KEYDOWN:
                #   if there is some input text
                if len(user_name) > 0:
                    if event.key == pygame.K_RETURN:
                        save(highscore)
                        return True
                    if event.key == pygame.K_BACKSPACE:
                        if len(user_name) > 0:
                            user_name = user_name[:-1]
                #   adding text
                # only letters, numbers, ".", "-" and maximum of 15 characters
                if len(user_name) < 15 and (event.unicode.isalnum() or event.unicode in ['.', '-']):
                    user_name += event.unicode
        #   data to save
        highscore = [[user_name, score, selected_ship, date]]
        #   rendering input
        # draw box around for text input
        pygame.draw.rect(screen, (230, 230, 230), text_box, int(width / 300))
        # input text
        text_surface = font_input.render(user_name, True, (230, 230, 230))
        # box is getting bigger with text (min. width, if is text wider, it is adding more width)
        text_box.w = max(width / 2.5, text_surface.get_width() + width / 50)
        # text
        text_rect = text_surface.get_rect()
        text_rect.centery = text_box.centery  # to get y center of text to y center of box
        text_rect.x = text_box.x + width / 100  # to get left side of text to wanted position
        # draw input text on wanted position
        screen.blit(text_surface, text_rect)
        # info about characters and rules when writing name
        screen.blit(font_info.render("maximum 15 characters", True, (150, 150, 150)),
                    (3.6 * width / 20, text_box.y + text_box.height * 1.3))
        screen.blit(font_info.render("only letters, numbers, dots, dashes", True, (150, 150, 150)),
                    (3.6 * width / 20, text_box.y + text_box.height * 1.7))
        #   cursor
        update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def statistics_menu(screen, joystick, cursor, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    font_scores_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.018 * width))  # loading font
    font_scores = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.014 * width))  # loading font

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("statistics")

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    buttons_num = 1
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.18, 0.05, 0.025, 'Back', screen,
                                sound, sound_volume, joystick, (0, 0))
    #   load the json file.
    highscores = load()
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))

        #   text "Leaderboard"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))

        #   BUTTON
        if back_button.draw_button_and_text(screen, True):
            return True
        #   display the high-scores.
        screen.blit(font_scores_title.render(game_text[0], True, (230, 230, 230)), (3.6 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[1], True, (230, 230, 230)), (8 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[2], True, (230, 230, 230)),
                    (11.8 * width / 20, 27 * height / 80))
        screen.blit(font_scores_title.render(game_text[3], True, (230, 230, 230)), (15 * width / 20, 27 * height / 80))
        y_position = list(range(32, 62, 3))  # the number of numbers here makes the number of names in the scoreboard
        for (hi_name, hi_score, hi_selected_ship, hi_date), y in zip(highscores, y_position):
            screen.blit(font_scores.render(f'{hi_name}', True, (160, 160, 160)), (3.6 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_score}', True, (160, 160, 160)), (8 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_selected_ship}', True, (160, 160, 160)),
                        (11.8 * width / 20, y * height / 80))
            screen.blit(font_scores.render(f'{hi_date}', True, (160, 160, 160)), (15 * width / 20, y * height / 80))

        #   event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(1, buttons_num)
            if action == 'exit' or action == 'enter':
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                return

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def main_menu(screen, joystick, cursor, clock, cursor_group):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_music = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("main_menu")

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    buttons_num = 4
    play_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.32, 0.05, 0.025, game_text[0], screen,
                                sound, sound_volume, joystick, (0, 0))
    scoreboard_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                      "assets/images/button_02.png", 0.32, 0.05, 0.025, game_text[1], screen,
                                      sound, sound_volume, joystick, (0, 1))
    aboutgame_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.32, 0.05, 0.025, game_text[2], screen,
                                     sound, sound_volume, joystick, (0, 2))
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.32, 0.05, 0.025, game_text[3], screen,
                                sound, sound_volume, joystick, (0, 3))
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)),
                                    "assets/images/settings_button1.png",
                                    "assets/images/settings_button2.png", 0.04, 0.04, 0.01, '', screen,
                                    sound, sound_volume, joystick)
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))

        #   text "Space shooter"            Pavel: Pozdeji by to místo toho možná chtělo nějakou grafickou náhradu
        screen.blit(font_title.render("Space shooter", True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   text "Soundtrack: Karl Casey @ White Bat Audio"

        text = font_music.render(game_text[4], True, (150, 150, 150))
        text_width = text.get_width()  # width of text
        screen.blit(text, (width - text_width * 1.02, 19.5 * height / 20))

        #   BUTTON
        play_button.update_text(game_text[0])
        scoreboard_button.update_text(game_text[1])
        aboutgame_button.update_text(game_text[2])
        quit_button.update_text(game_text[3])

        if play_button.draw_button_and_text(screen):
            return
        if scoreboard_button.draw_button_and_text(screen):
            statistics_menu(screen, joystick, cursor, clock, cursor_group)
        if aboutgame_button.draw_button_and_text(screen):
            about_game_menu(screen, joystick, cursor, clock, cursor_group)
        if quit_button.draw_button_and_text(screen):
            quit()
        if settings_button.draw_image_topRight(screen):
            settings_menu(screen, joystick, cursor, clock, cursor_group, background, "main")
            title, game_text = GameSetup.set_language("main_menu")

        # Event handling
        # keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(1, buttons_num)
            if action == 'settings':
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                settings_menu(screen, joystick, cursor, clock, cursor_group, background, "main")
                title, game_text = GameSetup.set_language("main_menu")
            elif action == 'enter':
                if joystick.position[1] == 0:
                    pygame.mixer.Channel(1).play(sound)
                    return
                elif joystick.position[1] == 1:
                    pygame.mixer.Channel(1).play(sound)
                    statistics_menu(screen, joystick, cursor, clock, cursor_group)
                elif joystick.position[1] == 2:
                    pygame.mixer.Channel(1).play(sound)
                    about_game_menu(screen, joystick, cursor, clock, cursor_group)
                elif joystick.position[1] == 3:
                    pygame.mixer.Channel(1).play(sound)
                    quit()
            elif action == 'exit':
                quit()

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def pause_menu(screen, joystick, clock, score, player, cursor, cursor_group, storage_items, installed_items):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))

    joystick.set_position(0, 0)

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent

    # background
    background_copy = screen.copy()
    surface.fill((0, 0, 0, 170))  # fill the whole screen with black transparent color

    # ship
    ship_surf = player.image_non_rot
    # new_width = int(ship_surf.get_width() * width / 809)
    # new_height = int(ship_surf.get_height() * height / 455)
    new_width = int(ship_surf.get_width() * 1.8)
    new_height = int(ship_surf.get_height() * 1.8)
    ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
    ship_rect = ship_surf.get_rect(center=(width / 1.3, height / 1.7))
    ship_mask = pygame.mask.from_surface(ship_surf)
    ship_surf_transparent = ship_surf.copy()
    ship_surf_transparent.set_alpha(100)

    # settings
    settings_icon = pygame.image.load("assets/images/settings_icon_big.png").convert_alpha()
    new_width = int(settings_icon.get_width() * width / 1234)
    new_height = int(settings_icon.get_height() * height / 806)
    settings_icon = pygame.transform.scale(settings_icon, (new_width, new_height))
    settings_rect = settings_icon.get_rect()
    settings_rect.centerx = ship_rect.centerx
    settings_rect.centery = ship_rect.centery + height / 17

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((width / 86.4, height / 153.6)))

    # text
    title, game_text = GameSetup.set_language("pause")

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    resume_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                  "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[0], screen,
                                  sound, sound_volume, joystick, (0, 0))
    main_menu_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[1], screen,
                                     sound, sound_volume, joystick, (0, 1))
    quit_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.3, 0.05, 0.025, game_text[2], screen,
                                sound, sound_volume, joystick, (0, 2))
    settings_button = button.Button(149 * (width / 150), width - (149 * (width / 150)),
                                    "assets/images/settings_button1.png", "assets/images/settings_button2.png", 0.04,
                                    0.04, 0.01, '', screen, sound, sound_volume, joystick)
    while True:
        # actual ship
        ship_surf = player.image_non_rot
        new_width = int(ship_surf.get_width() * 1.8)
        new_height = int(ship_surf.get_height() * 1.8)
        ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
        ship_surf_transparent = ship_surf.copy()
        ship_surf_transparent.set_alpha(100)

        # render background
        screen.blit(background_copy, (0, 0))
        screen.blit(surface, (0, 0))

        # update buttons
        resume_button.update_text(game_text[0])
        main_menu_button.update_text(game_text[1])
        quit_button.update_text(game_text[2])

        # mouse
        mouse_pos = pygame.mouse.get_pos()

        if ship_mask.overlap(mouse_mask, (mouse_pos[0] - ship_rect.x, mouse_pos[1] - ship_rect.y)):
            over_ship = True
        else:
            over_ship = False
        if over_ship and not joystick.active or joystick.position[0] == 1 and joystick.active:
            screen.blit(ship_surf_transparent, ship_rect)
            screen.blit(settings_icon, settings_rect)
        else:
            screen.blit(ship_surf, ship_rect)

        #   text "Main Menu"
        screen.blit(font_title.render(title, True, (230, 230, 230)), (3.6 * width / 20, 3.4 * height / 20))
        #   BUTTON
        if resume_button.draw_button_and_text(screen, joystick):
            return False
        if main_menu_button.draw_button_and_text(screen, joystick):
            return True
        if quit_button.draw_button_and_text(screen, joystick):
            quit()
        if settings_button.draw_image_topRight(screen):
            settings_menu(screen, joystick, cursor, clock, cursor_group, background_copy, "pause")
            title, game_text = GameSetup.set_language("pause")

        #   closing pause  menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                if over_ship:
                    upgrade_menu(screen, joystick, clock, player, cursor, cursor_group, storage_items, installed_items)
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # render score
        render_score(screen, score, 230, 230, 230)

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(2, 3)
            if action == 'settings':
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                settings_menu(screen, joystick, cursor, clock, cursor_group, background_copy, "pause")
                title, game_text = GameSetup.set_language("pause")
            elif action == 'enter':
                if joystick.position == (0, 0):
                    pygame.mixer.Channel(1).play(sound)
                    return False
                elif joystick.position == (0, 1):
                    pygame.mixer.Channel(1).play(sound)
                    return True
                elif joystick.position == (0, 2):
                    pygame.mixer.Channel(1).play(sound)
                    quit()
                elif joystick.position[0] == 1:
                    upgrade_menu(screen, joystick, clock, player, cursor, cursor_group, storage_items, installed_items)

            elif action == 'exit':
                pygame.mixer.Channel(1).play(sound)
                return False

            if action == 'settings':
                pass

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def upgrade_menu(screen, joystick, clock, player, cursor, cursor_group, storage_items, installed_items):
    player.update_animation()
    width, height = screen.get_size()
    joystick.set_position(3, 0)

    # background
    background = pygame.image.load("assets/images/Background.png").convert_alpha()
    background = pygame.transform.scale(background, (width, height))
    storage = pygame.image.load("assets/images/storage.png").convert_alpha()

    # storage background
    storage = pygame.transform.scale(storage, (width, height))

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((10, 10)))

    # bin
    thrash_bin = pygame.image.load("assets/images/thrash_bin.png").convert_alpha()
    new_width = int(thrash_bin.get_width() * width / 1536)
    new_height = int(thrash_bin.get_height() * height / 864)
    thrash_bin = pygame.transform.scale(thrash_bin, (new_width, new_height))
    thrash_bin_rect = thrash_bin.get_rect()
    thrash_bin_rect.center = (width / 1536 * 1400, height / 864 * 740)

    enlarged_thrash_bin_size = pygame.Vector2(thrash_bin.get_size()) * 1.3
    enlarged_thrash_bin_surf = pygame.transform.scale(thrash_bin, enlarged_thrash_bin_size)
    enlarged_thrash_bin_rect = enlarged_thrash_bin_surf.get_rect()
    enlarged_thrash_bin_rect.center = thrash_bin_rect.center
    thrash_bin_mask = pygame.mask.from_surface(thrash_bin)
    over_thrash_bin = False

    # description
    font_description = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(28 * width / 1536))

    # modules
    module_white = pygame.image.load("assets/images/module_white.png").convert_alpha()
    new_width = int(module_white.get_width() * width / 1536)
    new_height = int(module_white.get_height() * height / 864)
    module_white = pygame.transform.scale(module_white, (new_width, new_height))

    module_black = pygame.image.load("assets/images/module_black.png").convert_alpha()
    new_width = int(module_black.get_width() * width / 1536)
    new_height = int(module_black.get_height() * height / 864)
    module_black = pygame.transform.scale(module_black, (new_width, new_height))

    # text
    game_text = None
    for language in GameSetup.languages:
        if language['language'] == GameSetup.language:
            game_text = language['text']['upgrade']['content']

    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(32 * width / 1536))

    # ship parts
    ship_parts_images = {
        "weapons": [],
        "cooling": [],
        "shield": [],
        "repair_module": [],
        "booster": []
    }
    for module in ship_parts_images.keys():
        for i in range(3):
            ship_parts_images[module].append(pygame.image.load(f"assets/images/{module}{i}.png").convert_alpha())

    # picked mark
    picked_mark = pygame.image.load("assets/images/picked_mark.png").convert_alpha()
    new_width = int(picked_mark.get_width() * width / 1536)
    new_height = int(picked_mark.get_height() * height / 864)
    picked_mark = pygame.transform.scale(picked_mark, (new_width, new_height))
    picked_mark_active = 1

    # ship
    ship_surf = player.build_ship(player.type)
    pos = (width / 1536 * 450, height / 864 * 320)
    new_width = int(ship_surf.get_width() * 2.3 * width / 1536)
    new_height = int(ship_surf.get_height() * 2.3 * height / 864)
    ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
    ship_rect = ship_surf.get_rect(center=pos)
    ship_mask = pygame.mask.from_surface(ship_surf)
    over_ship = False
    ship_surf_transparent = ship_surf.copy()
    ship_surf_transparent.set_alpha(100)

    # settings
    controller_icon = pygame.image.load("assets/images/controller.png").convert_alpha()
    controller_new_width = int(controller_icon.get_width() * width / 1536)
    controller_new_height = int(controller_icon.get_height() * height / 864)
    controller_icon = pygame.transform.scale(controller_icon, (controller_new_width, controller_new_height))
    controller_rect = controller_icon.get_rect()
    controller_rect.centerx = ship_rect.centerx
    controller_rect.centery = ship_rect.centery + height / 864 * 50

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    x = width / 1536 * 932
    y = height / 864 * 78
    storage_buttons = [(x, y), (x + width / 1536 * 260, y), (x, y + height / 864 * 260),
                       (x + width / 1536 * 260, y + height / 864 * 260)]
    module_buttons = {
        "weapons": (width / 1536 * 90, height / 864 * 118, True),
        "cooling": (width / 1536 * 635, height / 864 * 118, True),
        "shield": (width / 1536 * 85, height / 864 * 392, True),
        "repair_module": (width / 1536 * 640, height / 864 * 392, True),
        "booster": (width / 1536 * 365, height / 864 * 590, True)
    }
    max_level = 3

    while True:
        # render background
        screen.blit(background, (0, 0))
        screen.blit(storage, (0, 0))
        if over_ship and not joystick.active or joystick.position[0] == 1 and joystick.active:
            screen.blit(ship_surf_transparent, ship_rect)
            screen.blit(controller_icon, controller_rect)
        else:
            screen.blit(ship_surf, ship_rect)
        if over_thrash_bin:
            screen.blit(enlarged_thrash_bin_surf, enlarged_thrash_bin_rect)
        else:
            screen.blit(thrash_bin, thrash_bin_rect)

        description = None
        max_level_reached = False
        item_stat_color = 'white'
        for module, level in player.ship_parts.items():
            if 0 < picked_mark_active <= len(storage_items):
                if module == storage_items[picked_mark_active - 1].upgrade_type:
                    if module == 'weapons':
                        current_dmg = player.proj_dmg_array[level]
                        current_fire_rate = player.fire_rate_array[level]
                        current_overheat = player.overheat_array[level]

                        if storage_items[picked_mark_active - 1].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_dmg = None
                                item_fire_rate = None
                                item_overheat = None
                            else:
                                item_dmg = player.proj_dmg_array[level + 1]
                                item_fire_rate = player.fire_rate_array[level + 1]
                                item_overheat = player.overheat_array[level + 1]
                        else:
                            item_dmg = player.proj_dmg_array[storage_items[picked_mark_active - 1].level]
                            item_fire_rate = player.fire_rate_array[storage_items[picked_mark_active - 1].level]
                            item_overheat = player.overheat_array[storage_items[picked_mark_active - 1].level]

                        description = {'DMG:': (current_dmg, item_dmg),
                                       'Fire rate:': (current_fire_rate, item_fire_rate),
                                       'Overheat:': (current_overheat, item_overheat)}

                    elif module == 'cooling':
                        current_cooling = player.cooling_array[level]

                        if storage_items[picked_mark_active - 1].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_cooling = None
                            else:
                                item_cooling = player.cooling_array[level + 1]
                        else:
                            item_cooling = player.cooling_array[storage_items[picked_mark_active - 1].level]

                        description = {'Cooling:': (current_cooling, item_cooling)}

                    elif module == 'repair_module':
                        current_regeneration = player.regeneration_array[level]

                        if storage_items[picked_mark_active - 1].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_regeneration = None
                            else:
                                item_regeneration = player.regeneration_array[level + 1]
                        else:
                            item_regeneration = player.regeneration_array[storage_items[picked_mark_active - 1].level]

                        description = {'Regeneration:': (current_regeneration, item_regeneration)}

                    elif module == 'shield':
                        current_max_hp = player.max_hp_array[level]
                        current_collision_dmg = player.dmg_array[level]

                        if storage_items[picked_mark_active - 1].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_max_hp = None
                                item_collision_dmg = None
                            else:
                                item_max_hp = player.max_hp_array[level + 1]
                                item_collision_dmg = player.dmg_array[level + 1]
                        else:
                            item_max_hp = player.max_hp_array[storage_items[picked_mark_active - 1].level]
                            item_collision_dmg = player.dmg_array[storage_items[picked_mark_active - 1].level]

                        description = {'Max HP:': (current_max_hp, item_max_hp),
                                       'Collision DMG:': (current_collision_dmg, item_collision_dmg)}

                    elif module == 'booster':
                        current_acceleration = player.acceleration_array[level]

                        if storage_items[picked_mark_active - 1].upgradable:
                            if level + 1 > max_level:
                                max_level_reached = True
                                item_acceleration = None
                            else:
                                item_acceleration = player.acceleration_array[level + 1]
                        else:
                            item_acceleration = player.acceleration_array[storage_items[picked_mark_active - 1].level]

                        description = {'Acceleration:': (current_acceleration, item_acceleration)}
        if description:
            for i, (stat_name, (current_stat, item_stat)) in enumerate(description.items()):
                screen.blit(font_description.render(stat_name, True, 'white'),
                            (width / 1536 * 660, height / 864 * 650 + i * 60))
                if max_level_reached:
                    screen.blit(font_description.render(str(current_stat), True, 'white'),
                                (width / 1536 * 1050, height / 864 * 650 + i * 60))
                else:
                    screen.blit(font_description.render(str(current_stat) + ' → ', True, 'white'),
                                (width / 1536 * 1050, height / 864 * 650 + i * 60))
                    font_width = font_description.render(str(current_stat) + ' → ', True, 'white').get_width()
                    if current_stat > item_stat:
                        item_stat_color = 'red'
                    elif current_stat < item_stat:
                        item_stat_color = 'green'
                    screen.blit(font_description.render(str(item_stat), True, item_stat_color),
                                (width / 1536 * 1050 + font_width, height / 864 * 650 + i * 60))

        # rendering storage items
        for i, item in enumerate(storage_items):
            # calculating centers of rects
            storage_button_x = storage_buttons[i][0] + width / 1536 * 132
            storage_button_y = storage_buttons[i][1] + height / 864 * 130

            item_rect = item.unscaled_image.get_rect()
            item_x = storage_button_x - item_rect.width // 2
            item_y = storage_button_y - item_rect.height // 2
            screen.blit(item.unscaled_image, (item_x, item_y))

        # rendering modules
        for i, (module, (x, y, active)) in enumerate(module_buttons.items()):
            module_rect = module_white.get_rect()
            module_rect.x = x
            module_rect.y = y
            if active:
                screen.blit(module_white, module_rect)
            else:
                screen.blit(module_black, module_rect)

            text = font_title.render(game_text[i], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = module_rect.centerx
            text_rect.y = module_rect.y + height / 864 * 190
            screen.blit(text, text_rect)

        # rendering installed items
        for module, i in player.ship_parts.items():
            # calculating centers of module rects
            if i > 0:
                module_button_x, module_button_y, active = module_buttons[module]
                module_button_x_center = module_button_x + width / 1536 * 93
                module_button_y_center = module_button_y + height / 864 * 90

                item_rect = ship_parts_images[module][player.ship_parts[module] - 1].get_rect()
                item_x = module_button_x_center - item_rect.width // 2
                item_y = module_button_y_center - item_rect.height // 2
                screen.blit(ship_parts_images[module][player.ship_parts[module] - 1], (item_x, item_y))

        # rendering picked mark
        if picked_mark_active > 0:
            # calculating centers of storage button rects
            storage_button_x = storage_buttons[picked_mark_active - 1][0] + width / 1536 * 132
            storage_button_y = storage_buttons[picked_mark_active - 1][1] + height / 864 * 130

            picked_mark_rect = picked_mark.get_rect()
            picked_mark_x = storage_button_x - picked_mark_rect.width // 2
            picked_mark_y = storage_button_y - picked_mark_rect.height // 2
            screen.blit(picked_mark, (picked_mark_x, picked_mark_y))
        elif picked_mark_active < 0:
            # calculating centers of module button rects
            key = list(module_buttons.keys())[-picked_mark_active - 1]
            module_rect = module_white.get_rect()
            module_rect.x = module_buttons[key][0]
            module_rect.y = module_buttons[key][1]

            picked_mark_rect = picked_mark.get_rect()
            picked_mark_rect.center = module_rect.center
            screen.blit(picked_mark, picked_mark_rect)

        # searching if the item type fits the part of the ship, the ones that doesn't fit are unactive
        for module, (x, y, active) in module_buttons.items():
            if 0 < picked_mark_active <= len(storage_items):
                if module == storage_items[picked_mark_active - 1].upgrade_type:
                    module_buttons[module] = (x, y, True)
                else:
                    module_buttons[module] = (x, y, False)
            else:
                module_buttons[module] = (x, y, True)

        mouse_pos = pygame.mouse.get_pos()
        if thrash_bin_mask.overlap(mouse_mask, (mouse_pos[0] - thrash_bin_rect.x, mouse_pos[1] - thrash_bin_rect.y)):
            over_thrash_bin = True
        else:
            over_thrash_bin = False
        if ship_mask.overlap(mouse_mask, (mouse_pos[0] - ship_rect.x, mouse_pos[1] - ship_rect.y)):
            over_ship = True
        else:
            over_ship = False

        # closing upgrade menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                player.image_non_rot_orig = player.build_ship(player.type)
                player.image_non_rot_orig = pygame.transform.scale_by(player.image_non_rot_orig, player.img_scale_ratio)
                player.image_non_rot_orig = player.scale_image(player.image_non_rot_orig)
                player.image_non_rot = player.image_non_rot_orig
                player.image = player.image_non_rot
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.QUIT:  # to quit game
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # collision with thrash bin
                if over_thrash_bin and picked_mark_active <= len(storage_items):
                    storage_items.pop(picked_mark_active - 1)
                if over_ship:
                    menu_cockpit(screen, joystick, clock, player, cursor, cursor_group)  # entering cockpit menu

                # collision with storage rects
                for i, (x, y) in enumerate(storage_buttons):
                    rect = pygame.Rect(x, y, width / 1536 * 260, height / 864 * 260)
                    if rect.collidepoint(mouse_pos):
                        picked_mark_active = i + 1
                        break

                # collision with module rects
                for module, (x, y, active) in module_buttons.items():
                    rect = pygame.Rect(x, y, width / 1536 * 260, height / 864 * 260)
                    if rect.collidepoint(mouse_pos):
                        if picked_mark_active <= len(storage_items):
                            if storage_items[picked_mark_active - 1].upgradable:
                                if installed_items[module]:
                                    if player.ship_parts[module] + 1 <= max_level:
                                        installed_items[module].level_up()
                                        player.ship_parts[module] += 1
                                        storage_items.pop(picked_mark_active - 1)
                                    else:
                                        storage_items.append(installed_items[module])
                                        installed_items[module] = None
                                        player.ship_parts[module] = 0
                                else:
                                    if module == storage_items[picked_mark_active - 1].upgrade_type:
                                        player.ship_parts[module] += 1
                                        installed_items[module] = ShipUpgrade((0, 0), module, False)
                                        storage_items.pop(picked_mark_active - 1)
                            else:
                                if installed_items[module]:
                                    storage_items.append(installed_items[module])
                                    installed_items[module] = None
                                    player.ship_parts[module] = 0
                                else:
                                    if picked_mark_active - 1 <= len(storage_items):
                                        if module == storage_items[picked_mark_active - 1].upgrade_type:
                                            installed_items[module] = storage_items[picked_mark_active - 1]
                                            player.ship_parts[module] = installed_items[module].level
                                            storage_items.pop(picked_mark_active - 1)
                        else:
                            if installed_items[module]:
                                storage_items.append(installed_items[module])
                                installed_items[module] = None
                                player.ship_parts[module] = 0

                player.image_non_rot_orig = player.build_ship(player.type)
                player.image_non_rot_orig = pygame.transform.scale_by(player.image_non_rot_orig, player.img_scale_ratio)
                player.image_non_rot_orig = player.scale_image(player.image_non_rot_orig)
                player.image_non_rot = player.image_non_rot_orig
                player.image = player.image_non_rot

                player.update_animation()
                ship_surf = player.build_ship(player.type)
                ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False
            action = joystick.menu_control(5, 3)

            # finding the correct mark
            if joystick.position[0] >= 3:
                if joystick.position == (3, 0):
                    picked_mark_active = 1
                elif joystick.position == (3, 1):
                    picked_mark_active = 3
                elif joystick.position == (4, 0):
                    picked_mark_active = 2
                elif joystick.position == (4, 1):
                    picked_mark_active = 4
                elif joystick.position == (3, 2):
                    joystick.position = (3, 0)
                elif joystick.position == (4, 2):
                    joystick.position = (4, 0)
            else:
                if joystick.position == (0, 0):
                    picked_mark_active = -1
                elif joystick.position == (0, 1):
                    picked_mark_active = -3
                elif joystick.position == (0, 2):
                    if joystick.last_position == (0, 1):
                        joystick.position = (1, 2)
                    else:
                        joystick.position = (0, 1)
                elif joystick.position == (2, 2):
                    if joystick.last_position == (2, 1):
                        joystick.position = (1, 2)
                    else:
                        joystick.position = (2, 1)
                elif joystick.position[1] == 2:
                    picked_mark_active = -5
                    joystick.set_position(1, 2)
                elif joystick.position[0] == 1:
                    if joystick.position[1] == 1 and joystick.last_position[1] == 0:
                        joystick.set_position(1, 2)
                        over_ship = False
                    else:
                        over_ship = True
                        picked_mark_active = 0
                elif joystick.position == (2, 0):
                    picked_mark_active = -2
                elif joystick.position == (2, 1):
                    picked_mark_active = -4

            if action == 'enter':
                # entering cockpit
                if over_ship:
                    menu_cockpit(screen, joystick, clock, player, cursor, cursor_group)

                # logic behind moving items
                for module, (x, y, active) in module_buttons.items():
                    if joystick.position[0] >= 3:
                        if active:
                            if picked_mark_active <= len(storage_items):
                                if storage_items[picked_mark_active - 1].upgradable:
                                    if installed_items[module]:
                                        if player.ship_parts[module] + 1 <= max_level:
                                            installed_items[module].level_up()
                                            player.ship_parts[module] += 1
                                            storage_items.pop(picked_mark_active - 1)
                                        else:
                                            storage_items.append(installed_items[module])
                                            installed_items[module] = None
                                            player.ship_parts[module] = 0
                                    else:
                                        if module == storage_items[picked_mark_active - 1].upgrade_type:
                                            player.ship_parts[module] += 1
                                            installed_items[module] = ShipUpgrade((0, 0), module, False)
                                            storage_items.pop(picked_mark_active - 1)
                                else:
                                    if installed_items[module]:
                                        storage_items.append(installed_items[module])
                                        installed_items[module] = None
                                        player.ship_parts[module] = 0
                                    else:
                                        if picked_mark_active <= len(storage_items):
                                            if module == storage_items[picked_mark_active - 1].upgrade_type:
                                                installed_items[module] = storage_items[picked_mark_active - 1]
                                                player.ship_parts[module] = installed_items[module].level
                                                storage_items.pop(picked_mark_active - 1)
                    else:
                        key = list(module_buttons.keys())[-picked_mark_active - 1]
                        if installed_items[key]:
                            storage_items.append(installed_items[key])
                            installed_items[key] = None
                            player.ship_parts[key] = 0

                player.image_non_rot_orig = player.build_ship(player.type)
                player.image_non_rot_orig = pygame.transform.scale_by(player.image_non_rot_orig, player.img_scale_ratio)
                player.image_non_rot_orig = player.scale_image(player.image_non_rot_orig)
                player.image_non_rot = player.image_non_rot_orig
                player.image = player.image_non_rot

                player.update_animation()
                ship_surf = player.build_ship(player.type)
                ship_surf = pygame.transform.scale(ship_surf, (new_width, new_height))

            elif action == 'square':
                if storage_items:
                    storage_items.pop(picked_mark_active - 1)

            elif action == 'exit':
                return False

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        player.update_parameters()

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def menu_cockpit(screen, joystick, clock, player, cursor, cursor_group):
    width, height = screen.get_size()
    in_minigame = False

    # hp
    hp = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/cockpit/hp{i}.png").convert_alpha()
        new_width = int(img.get_width() * width / 1536)
        new_height = int(img.get_height() * height / 864)
        img = pygame.transform.scale(img, (new_width, new_height))
        hp.append(img)

    # background
    background_image = Background("cockpit", 5, (30, 100))
    background_group = pygame.sprite.Group()
    background_group.add(background_image)

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    # button
    joystick.set_position(0, 0)
    play_button = button.Button(width / 1536 * 650, height / 864 * 330, "assets/images/cockpit/button_01.png",
                                "assets/images/cockpit/button_02.png", 0.15, 0.05,
                                0.021, '', screen, sound, sound_volume, joystick, (0, 0))

    (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
     mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame(joystick)

    if not joystick.active:
        cursor.set_cursor()

    while True:

        # closing upgrade menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to continue play
                if in_minigame:
                    in_minigame = False
                    cursor.set_cursor()
                    (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
                     mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame(
                        joystick)
                else:
                    return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.QUIT:  # to quit game
                quit()
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(1, 1)
            if action == 'enter':
                in_minigame = True
            elif action == 'exit':
                if in_minigame:
                    in_minigame = False
                    cursor.set_cursor()
                    (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
                     mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame(
                        joystick)
                else:
                    return False

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        if in_minigame:
            # updating groups
            update_groups(
                [background_group, mini_player_projectile_group, mini_enemy_projectile_group, mini_enemy_group,
                 mini_player_group, mini_spawner_group, mini_explosion_group], screen)

            screen.blit(hp[int(mini_player.hp)], (width / 1536 * 520, height / 864 * 500))

            # updating cursor
            update_groups([cursor_group], screen)

            handle_collisions(joystick, mini_item_group, mini_player_group, False, mini_enemy_group, False,
                              mini_explosion_group)
            handle_collisions(joystick, mini_item_group, mini_player_projectile_group, True, mini_enemy_group, False,
                              mini_explosion_group)
            handle_collisions(joystick, mini_item_group, mini_enemy_projectile_group, True, mini_player_group, False,
                              mini_explosion_group)
            handle_collisions(joystick, mini_item_group, mini_player_projectile_group, True,
                              mini_enemy_projectile_group, True,
                              mini_explosion_group)

            cursor.check_cursor()

            # FPS lock and adding time
            time_diff = clock.tick(GameSetup.fps) / 1000
            update_time([mini_player_group, mini_enemy_group, mini_item_group, mini_spawner_group], time_diff)

            if not mini_player_group and not mini_explosion_group:
                #   death_menu
                in_minigame = False
                cursor.set_cursor()
                (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
                 mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group) = set_minigame(
                    joystick)
        else:
            screen.blit(mini_player.image, mini_player.rect)
            update_groups([background_group], screen)
            screen.blit(hp[3], (width / 1536 * 520, height / 864 * 500))
            if not joystick.active:
                update_groups([cursor_group], screen)
            if play_button.draw_button_and_text(screen):
                in_minigame = True

        pygame.display.flip()
        clock.tick(GameSetup.fps)


def set_minigame(joystick):
    # groups
    mini_enemy_group = pygame.sprite.Group()
    mini_spawner_group = pygame.sprite.Group()
    mini_item_group = pygame.sprite.Group()
    mini_player_projectile_group = pygame.sprite.Group()
    mini_enemy_projectile_group = pygame.sprite.Group()
    mini_explosion_group = pygame.sprite.Group()
    mini_player_group = pygame.sprite.Group()

    # player
    mini_player = MiniPlayer(joystick, mini_player_projectile_group)
    mini_player_group.add(mini_player)

    mini_zarovka_spawner = EnemySpawner(mini_enemy_group, "minizarovka", 3, mini_player)
    mini_spawner_group.add(mini_zarovka_spawner)

    return (mini_enemy_group, mini_spawner_group, mini_item_group, mini_player_projectile_group,
            mini_enemy_projectile_group, mini_explosion_group, mini_player, mini_player_group)


def ship_menu(screen, joystick, cursor, clock, cursor_group):
    width, height = screen.get_size()
    joystick.set_position(1, 0)

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("ship_select")

    #   text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    text = font_title.render(title, True, (230, 230, 230))
    text_rect = text.get_rect()
    text_rect.centerx = width / 2
    text_rect.y = 3.4 * height / 20

    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    buttons_num = 3
    Light_button = button.Button(2 * width / 8, 8 * height / 16, "assets/images/player_light/vlod_player_light.png",
                                 "assets/images/player_light/vlod_player_light.png",
                                 0.08, 0.1, 0.02, 'Light', screen, sound, sound_volume, joystick, (0, 0))
    Mid_button = button.Button(4 * width / 8, 8 * height / 16, "assets/images/player_mid/vlod_player_mid.png",
                               "assets/images/player_mid/vlod_player_mid.png",
                               0.09, 0.1, 0.02, 'Mid', screen, sound, sound_volume, joystick, (1, 0))
    Tank_button = button.Button(6 * width / 8, 8 * height / 16, "assets/images/player_tank/vlod_player_tank.png",
                                "assets/images/player_tank/vlod_player_tank.png",
                                0.08, 0.1, 0.02, 'Tank', screen, sound, sound_volume, joystick, (2, 0))
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Ship selection"
        screen.blit(text, text_rect)
        #   text of ships properties
        #   button
        if Light_button.draw_image_in_center(screen, game_text):
            return 1
        if Mid_button.draw_image_in_center(screen, game_text):
            return 2
        if Tank_button.draw_image_in_center(screen, game_text):
            return 3
        #   Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            elif event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound.set_volume(sound_volume * GameSetup.effects_volume)
                    pygame.mixer.Channel(1).play(sound)
                    return 0
            elif event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(buttons_num, 1)
            if action == 'enter':
                return joystick.position[0] + 1

            elif action == 'exit':
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                return 0

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def death_menu(screen, joystick, cursor, clock, cursor_group, score, ship_number):
    width, height = screen.get_size()
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))
    font_score = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.025 * width))

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 230))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("game_over")
    title_surf = font_title.render(title, True, (230, 230, 230))
    title_rect = title_surf.get_rect()
    title_rect.centerx = GameSetup.width / 2
    title_rect.y = 100

    #   sound
    sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    save_name_button = button.Button(3.6 * width / 20, 32 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.37, 0.05, 0.025, game_text[1], screen,
                                     sound, sound_volume, joystick, (0, 0))
    restart_button = button.Button(3.6 * width / 20, 41 * height / 80, "assets/images/button_01.png",
                                   "assets/images/button_02.png", 0.37, 0.05, 0.025, game_text[2], screen,
                                   sound, sound_volume, joystick, (0, 1))
    main_menu_button = button.Button(3.6 * width / 20, 50 * height / 80, "assets/images/button_01.png",
                                     "assets/images/button_02.png", 0.37, 0.05, 0.025, game_text[3], screen,
                                     sound, sound_volume, joystick, (0, 2))
    quit_button = button.Button(3.6 * width / 20, 59 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.37, 0.05, 0.025, game_text[4], screen,
                                sound, sound_volume, joystick, (0, 3))

    #   a variable that makes it possible to make the save name button disappear after saving a name
    save_name_clicked = False
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "Game over" and "score"
        screen.blit(title_surf, title_rect)
        score_text = game_text[0] + str(score)
        screen.blit(font_score.render(score_text, True, (230, 230, 230)), (3.6 * width / 20, 5.7 * height / 20))
        #   button
        if not save_name_clicked:
            if save_name_button.draw_button_and_text(screen):
                save_name_clicked = save_name_menu(screen, joystick, clock, cursor_group, score, ship_number)
                # save_name_clicked = True
        if restart_button.draw_button_and_text(screen):
            return False
        if main_menu_button.draw_button_and_text(screen):
            return True
        if quit_button.draw_button_and_text(screen):
            quit()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(1, 4)
            if action == 'enter':
                if joystick.position == (0, 0):
                    if not save_name_clicked:
                        pygame.mixer.Channel(1).play(sound)
                        save_name_clicked = save_name_menu(screen, joystick, clock, cursor_group, score, ship_number)
                elif joystick.position == (0, 1):
                    pygame.mixer.Channel(1).play(sound)
                    return False
                elif joystick.position == (0, 2):
                    pygame.mixer.Channel(1).play(sound)
                    return True
                elif joystick.position == (0, 3):
                    pygame.mixer.Channel(1).play(sound)
                    quit()

            elif action == 'exit':
                pygame.mixer.Channel(1).play(sound)
                return False

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()


def about_game_menu(screen, joystick, cursor, clock, cursor_group):
    width, height = screen.get_size()
    #   variable for scroll
    record = True
    y_scroll = 0

    # mouse mask
    mouse_mask = pygame.mask.from_surface(pygame.Surface((10, 10)))

    #   text
    # variables for text
    spaceBetween = 0.009 * width
    textAlignLeft = 0
    textAlignRight = 1
    textAlignCenter = 2
    textAlignBlock = 3

    # ship images
    vlod5L = pygame.image.load("assets/images/player_light/vlod_player_light.png").convert_alpha()
    vlod5L = pygame.transform.scale(vlod5L, (int(width * 0.08), int(width * 0.09)))  # transforming image
    vlod5L_pos = vlod5L.get_rect().center
    new_width = int(vlod5L.get_width() * 1.4)
    new_height = int(vlod5L.get_height() * 1.4)
    vlod5L_rect = vlod5L.get_rect(center=vlod5L_pos)
    enlarged_vlod5L = pygame.transform.scale(vlod5L, (new_width, new_height))
    enlarged_vlod5L_rect = enlarged_vlod5L.get_rect()
    enlarged_vlod5L_rect.center = vlod5L_rect.center
    vlod5L_mask = pygame.mask.from_surface(vlod5L)
    over_vlod5L = False

    vlod5 = pygame.image.load("assets/images/player_mid/vlod_player_mid.png").convert_alpha()
    vlod5 = pygame.transform.scale(vlod5, (int(width * 0.11), int(width * 0.12)))  # transforming image
    vlod5_pos = vlod5.get_rect().center
    new_width = int(vlod5.get_width() * 1.4)
    new_height = int(vlod5.get_height() * 1.4)
    vlod5_rect = vlod5.get_rect(center=vlod5_pos)
    enlarged_vlod5 = pygame.transform.scale(vlod5, (new_width, new_height))
    enlarged_vlod5_rect = enlarged_vlod5.get_rect()
    enlarged_vlod5_rect.center = vlod5_rect.center
    vlod5_mask = pygame.mask.from_surface(vlod5)
    over_vlod5 = False

    vlod5T = pygame.image.load("assets/images/player_tank/vlod_player_tank.png").convert_alpha()
    vlod5T = pygame.transform.scale(vlod5T, (int(width * 0.1), int(width * 0.12)))  # transforming image
    vlod5T_pos = vlod5T.get_rect().center
    new_width = int(vlod5T.get_width() * 1.4)
    new_height = int(vlod5T.get_height() * 1.4)
    vlod5T_rect = vlod5T.get_rect(center=vlod5T_pos)
    enlarged_vlod5T = pygame.transform.scale(vlod5T, (new_width, new_height))
    enlarged_vlod5T_rect = enlarged_vlod5T.get_rect()
    enlarged_vlod5T_rect.center = vlod5T_rect.center
    vlod5T_mask = pygame.mask.from_surface(vlod5T)
    over_vlod5T = False

    # fonts for text
    font_title = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.05 * width))  # loading font
    title_color = (230, 230, 230)
    font_subtitle = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.02 * width))  # loading font
    subtitle_height = font_subtitle.size("Tq")[1]  # height of font
    font_text = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.01 * width))  # loading font
    text_height = font_text.size("Tq")[1]  # height of font
    text_color = (180, 180, 180)
    font_name = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.012 * width))  # loading font
    name_color = (200, 200, 200)

    #   surface and background
    # surface
    surface = pygame.Surface(screen.get_size())  # creates a new surface of the same dimensions as screen
    surface = surface.convert_alpha()  # making surface transparent
    surface.fill((0, 0, 0, 80))  # fill the whole screen with black transparent color

    # background
    background = pygame.image.load("assets/images/Background.png")
    background = pygame.transform.scale(background, (width, height))
    background = pygame.Surface.convert(background)

    # text
    title, game_text = GameSetup.set_language("about_game")

    #   controls
    # keyboard
    font_control = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(0.015 * width))  # loading font

    keyboard = pygame.image.load("assets/images/skills_aboutGame/keyboard.png").convert_alpha()
    keyboard_size = keyboard.get_size()
    keyboard = pygame.transform.scale(keyboard, (int(0.4 * width / 1536 * keyboard_size[0]),
                                                 int(0.4 * height / 864 * keyboard_size[1])))
    keys = pygame.image.load("assets/images/skills_aboutGame/keys.png").convert_alpha()
    keys_size = keys.get_size()
    keys = pygame.transform.scale(keys, (int(0.8 * width / 1536 * keys_size[0]),
                                         int(0.8 * height / 864 * keys_size[1])))

    mouse = pygame.image.load("assets/images/skills_aboutGame/mouse.png").convert_alpha()
    mouse_size = mouse.get_size()
    mouse = pygame.transform.scale(mouse, (int(0.55 * width / 1536 * mouse_size[0]),
                                           int(0.6 * height / 864 * mouse_size[1])))

    # controller
    controller = pygame.image.load("assets/images/skills_aboutGame/controller.png").convert_alpha()
    controller_size = controller.get_size()
    controller = pygame.transform.scale(controller, (int(0.8 * width / 1536 * controller_size[0]),
                                                     int(0.8 * height / 864 * controller_size[1])))
    controller_close = pygame.image.load("assets/images/skills_aboutGame/controller_close_up.png").convert_alpha()
    controller_close_size = controller_close.get_size()
    controller_close = pygame.transform.scale(controller_close, (int(3 * width / 1536 * controller_close_size[0]),
                                                     int(3 * height / 864 * controller_close_size[1])))
    # sound
    sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")  # Load sound file
    sound_volume = 0.2
    sound.set_volume(sound_volume * GameSetup.effects_volume)

    #   create button instances
    buttons_num = 1
    back_button = button.Button(16 * width / 20, 70 * height / 80, "assets/images/button_01.png",
                                "assets/images/button_02.png", 0.18, 0.05, 0.025, game_text[33], screen,
                                sound, sound_volume, joystick, (0, 0))
    while True:
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        #   text "About game"
        screen.blit(font_title.render(title, True, (230, 230, 230)),
                    (3.6 * width / 20, (3.4 * height / 20) + y_scroll))

        mouse_pos = pygame.mouse.get_pos()

        #   BUTTON
        if back_button.draw_button_and_text(screen, True):
            return True
        #   about game text
        # about game

        textRect = pygame.Rect(3.6 * width / 20, (27 * height / 80) + y_scroll, 12 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[0], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # why was created
        textRect = pygame.Rect(3.6 * width / 20, lowest_value + spaceBetween * 2, 12 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[1], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # development team
        screen.blit(font_subtitle.render(game_text[2], True, title_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        screen.blit(font_text.render(game_text[3], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 2))
        screen.blit(font_text.render(game_text[4], True, text_color),
                    (8 * width / 20, lowest_value + spaceBetween * 2))
        lowest_value = lowest_value + spaceBetween * 2 + text_height
        screen.blit(font_text.render(game_text[5], True, text_color),
                    (3.6 * width / 20, lowest_value + spaceBetween))
        screen.blit(font_text.render(game_text[6], True, text_color), (8 * width / 20, lowest_value + spaceBetween))
        lowest_value = lowest_value + spaceBetween + text_height

        # controls
        if joystick.active:
            screen.blit(font_subtitle.render(game_text[7], True, title_color),
                        (3.6 * width / 20, lowest_value + spaceBetween * 4))
            screen.blit(controller, (width / 2.5, lowest_value + spaceBetween * 1.8))
            lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
            rect = controller_close.get_rect()
            rect.center = (width / 2, lowest_value + spaceBetween * 25)
            screen.blit(controller_close, rect)

            font = font_control.render(game_text[12], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (width / 2, lowest_value + spaceBetween * 7.5)
            screen.blit(font, rect)

            font = font_control.render(game_text[12], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.midleft = (1.5 * width / 2, lowest_value + spaceBetween * 23)
            screen.blit(font, rect)

            font = font_control.render(game_text[8], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (7.73 * width / 20, lowest_value + spaceBetween * 43)
            screen.blit(font, rect)

            font = font_control.render(game_text[11] + ' #1', True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.midright = (6.4 * width / 20, lowest_value + spaceBetween * 9)
            screen.blit(font, rect)

            font = font_control.render(game_text[11] + ' #2', True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.midright = (6 * width / 20, lowest_value + spaceBetween * 16)
            screen.blit(font, rect)

            font = font_control.render(game_text[9], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (11.6 * width / 20, lowest_value + spaceBetween * 43)
            screen.blit(font, rect)

            font = font_control.render(game_text[10], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (14.8 * width / 20, lowest_value + spaceBetween * 9)
            screen.blit(font, rect)

            lowest_value = lowest_value + spaceBetween * 11 + text_height * 30

        else:
            screen.blit(font_subtitle.render(game_text[7], True, title_color),
                        (3.6 * width / 20, lowest_value + spaceBetween * 4))
            screen.blit(keyboard, (width / 2.7, lowest_value + spaceBetween * 2.5))
            lowest_value = lowest_value + spaceBetween * 6 + subtitle_height
            screen.blit(keys, (8 * width / 40, lowest_value + spaceBetween * 3))
            screen.blit(mouse, (8 * width / 11.5, lowest_value + spaceBetween * 3.5))

            font = font_control.render(game_text[12], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (4.5 * width / 20, lowest_value + spaceBetween * 17)
            screen.blit(font, rect)

            font = font_control.render(game_text[8], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (7.73 * width / 20, lowest_value + spaceBetween * 17)
            screen.blit(font, rect)

            font = font_control.render(game_text[11], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (11.5 * width / 20, lowest_value + spaceBetween * 17)
            screen.blit(font, rect)

            font = font_control.render(game_text[10], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (14.6 * width / 20, lowest_value + spaceBetween)
            screen.blit(font, rect)

            font = font_control.render(game_text[9], True, text_color)
            size = font.get_size()
            rect = pygame.rect.Rect(0, 0, size[0], size[1])
            rect.center = (14.6 * width / 20, lowest_value + spaceBetween * 17)
            screen.blit(font, rect)

            lowest_value = lowest_value + spaceBetween * 14 + text_height * 5

        #   ships
        screen.blit(font_subtitle.render(game_text[13], True, title_color),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height

        # checking if mouse is over image
        if vlod5L_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5L_rect.x - vlod5L_rect.width / 2),
                                            mouse_pos[1] - (
                                                    lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - vlod5L_rect.height / 2))):
            over_vlod5L = True
        else:
            over_vlod5L = False

        # ship number 1
        if over_vlod5L:
            screen.blit(enlarged_vlod5L, ((5 * width / 20) + enlarged_vlod5L_rect.x - vlod5L_rect.width / 2,
                                          lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - enlarged_vlod5L_rect.height / 2))
        else:
            screen.blit(vlod5L, ((5 * width / 20) + vlod5L_rect.x - vlod5L_rect.width / 2,
                                 lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5L_rect.y - vlod5L_rect.height / 2))
        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]

        # write info about ship

        if over_vlod5L:
            text = font_name.render("LIGHT", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:

            text = font_name.render("LIGHT", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.25), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[21], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load("assets/images/skills_aboutGame/Q_dash_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.25), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[22], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_shield_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.25 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween

        # ship number 2

        # checking if mouse is over image
        if vlod5_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5_rect.x - vlod5_rect.width / 2),
                                           mouse_pos[1] - (
                                                   lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - vlod5_rect.height / 2))):
            over_vlod5 = True
        else:
            over_vlod5 = False

        # write image
        if over_vlod5:
            screen.blit(enlarged_vlod5, ((5 * width / 20) + enlarged_vlod5_rect.x - vlod5_rect.width / 2,
                                         lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - enlarged_vlod5_rect.height / 2))
        else:
            screen.blit(vlod5, ((5 * width / 20) + vlod5_rect.x - vlod5_rect.width / 2,
                                lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5_rect.y - vlod5_rect.height / 2))

        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("MID", True, name_color)

        if over_vlod5:
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[23], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/Q_rapidfire_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[24], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_blastshoot_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween

        # ship number 3

        if vlod5T_mask.overlap(mouse_mask, (mouse_pos[0] - ((5 * width / 20) + vlod5T_rect.x - vlod5T_rect.width / 2),
                                            mouse_pos[1] - (
                                                    lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - vlod5T_rect.height / 2))):
            over_vlod5T = True
        else:
            over_vlod5T = False

        # write image
        if over_vlod5T:
            screen.blit(enlarged_vlod5T, ((5 * width / 20) + enlarged_vlod5T_rect.x - vlod5T_rect.width / 2,
                                          lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - enlarged_vlod5T_rect.height / 2))
        else:
            screen.blit(vlod5T, ((5 * width / 20) + vlod5T_rect.x - vlod5T_rect.width / 2,
                                 lowest_value + 7 * spaceBetween + 4.5 * text_height + vlod5T_rect.y - vlod5T_rect.height / 2))

        # load info about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]

        # write info about ship
        if over_vlod5T:
            text = font_name.render("TANK", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color)
            textAcc_width = textAcc.get_width()  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        else:
            text = font_name.render("TANK", True, name_color)
            screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
            screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
            screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
            screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate'][0]}", True, text_color),
                        (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
            textAcc = font_text.render(f"{game_text[17]}{Ship_param['acceleration'][0]}", True, text_color)
            textAcc_width = textAcc.get_width() + 100  # getting width of text
            screen.blit(textAcc, (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
            screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                        (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        #   skills
        # skill Q
        text_skill_01 = font_text.render(game_text[19], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 4 * spaceBetween + text_height))
        text_skill_02 = font_text.render(game_text[25], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 4 * spaceBetween + text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/Q_speedboos_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 4 * spaceBetween + text_height + text_skill_02_height * 1.5))
        # skill E
        text_skill_01 = font_text.render(game_text[20], True, text_color)
        text_skill_01_width = text_skill_01.get_width()  # getting width of text
        screen.blit(text_skill_01,
                    (((7.5 * width / 20) + textAcc_width * 1.1), lowest_value + 7 * spaceBetween + 4 * text_height))
        text_skill_02 = font_text.render(game_text[26], True, text_color)
        text_skill_02_width = text_skill_02.get_width()  # getting width of text
        text_skill_02_height = text_skill_02.get_height()  # getting height of text
        screen.blit(text_skill_02, (((7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width),
                                    lowest_value + 7 * spaceBetween + 4 * text_height))
        image_Q = pygame.image.load(
            "assets/images/skills_aboutGame/E_gravitypulse_aboutGame.png").convert_alpha()  # load image
        image_Q = pygame.transform.scale(image_Q, (int(width * 0.03), int(width * 0.03)))  # transforming image
        image_width = image_Q.get_width()  # getting width of image
        screen.blit(image_Q, (
            (((
                      7.5 * width / 20) + textAcc_width * 1.1 + text_skill_01_width + text_skill_02_width / 2) - image_width / 2),
            lowest_value + 7 * spaceBetween + 4 * text_height + text_skill_02_height * 1.5))
        #   new lowest value
        lowest_value = lowest_value + 10 * spaceBetween + 7 * text_height + 4 * spaceBetween
        #   enemies
        screen.blit(font_subtitle.render(game_text[27], True, (230, 230, 230)),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + subtitle_height
        # enemy number 1
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[0]
        # write info about ship
        text = font_name.render("ZAROVKA", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))

        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[28], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # load and write image
        zarovka = pygame.image.load("assets/images/enemy/zarovka/zarovka.png")  # load image
        zarovka = pygame.transform.scale(zarovka, (int(width * 0.053), int(width * 0.08)))  # transforming image
        screen.blit(zarovka, ((5 * width / 20) - zarovka.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - zarovka.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 2
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[1]
        # write info about ship
        text = font_name.render("TANK", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[29], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # load and write image
        tank = pygame.image.load("assets/images/enemy/tank/tank.png")  # load image
        tank = pygame.transform.scale(tank, (int(width * 0.13), int(width * 0.12)))  # transforming image
        screen.blit(tank, ((5 * width / 20) - tank.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - tank.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 3
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[2]
        # write info about ship
        text = font_name.render("SNIPER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[15]}{Ship_param['proj_dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['fire_rate']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 8 * spaceBetween + 5 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 10 * spaceBetween + 6 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[30], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # load and write image
        sniper = pygame.image.load("assets/images/enemy/sniper/sniper.png")  # load image
        sniper = pygame.transform.scale(sniper, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(sniper, ((5 * width / 20) - sniper.get_rect().centerx, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - sniper.get_rect().centery))
        lowest_value += 3 * spaceBetween
        # enemy number 4
        # load info about ship from json
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        Ship_param = enemy_param[3]
        # write info about ship
        text = font_name.render("STEALER", True, name_color)
        screen.blit(text, ((5 * width / 20) - text.get_width() / 2, lowest_value + 2 * spaceBetween))
        screen.blit(font_text.render(f"{game_text[14]}{Ship_param['hp']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 4 * spaceBetween + text_height))
        lowest_value_firstText = lowest_value + 4 * spaceBetween + text_height  # variable for loading text in center
        screen.blit(font_text.render(f"{game_text[16]}{Ship_param['dmg']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 5 * spaceBetween + 2 * text_height))
        screen.blit(font_text.render(f"{game_text[17]}{Ship_param['acceleration']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 6 * spaceBetween + 3 * text_height))
        screen.blit(font_text.render(f"{game_text[18]}{Ship_param['max_velocity']}", True, text_color),
                    (7.5 * width / 20, lowest_value + 7 * spaceBetween + 4 * text_height))
        # writen info by myself
        textRect = pygame.Rect(7.5 * width / 20, lowest_value + 9 * spaceBetween + 5 * text_height, 8 * width / 20,
                               50)  # x-axis, y-axis, size on x-axis, size on y-axis
        lowest_value = drawText.drawText(screen, game_text[31], text_color, textRect, font_text, textAlignLeft, True,
                                         None)
        # load and write image
        stealer1 = pygame.image.load("assets/images/enemy/stealer/stealer1.png")  # load image
        stealer1 = pygame.transform.scale(stealer1, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer1, ((5 * width / 20) - stealer1.get_rect().width * 1.2, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - stealer1.get_rect().centery))
        # load and write image
        stealer2 = pygame.image.load("assets/images/enemy/stealer/stealer2.png")  # load image
        stealer2 = pygame.transform.scale(stealer2, (int(width * 0.06), int(width * 0.08)))  # transforming image
        screen.blit(stealer2, ((5 * width / 20) + stealer1.get_rect().width * 0.2, (
                lowest_value - lowest_value_firstText) / 2 + lowest_value_firstText - stealer2.get_rect().centery))
        lowest_value += 3 * spaceBetween
        #   thank you for playing our game
        screen.blit(font_name.render(game_text[32], True, (230, 230, 230)),
                    (3.6 * width / 20, lowest_value + spaceBetween * 4))
        lowest_value = lowest_value + spaceBetween * 4 + 6 * spaceBetween
        #   scroll bar
        # record of biggest lowest_value
        if record:
            lowest_value_first = lowest_value - height
            record = False
        # page ratio for slide bar
        page_ratio = (int(lowest_value_first - (lowest_value - height)) / (lowest_value_first))
        # bars proportions
        bar_pos = [39 / 40 * width, 7 / 40 * height]
        bar_size = [2 / 400 * width, 25 / 40 * height]
        # draw the bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(screen, (230, 230, 230), (bar_pos[0], bar_pos[1], bar_size[0], bar_size[1] * page_ratio))
        #   event handling
        for event in pg.event.get():
            if event.type == pygame.MOUSEWHEEL:  # 1 mean up, -1 mean down
                if event.y == 1 and y_scroll < 0:  # scroll up
                    if -y_scroll < (0.06 * height):
                        y_scroll = 0
                    else:
                        y_scroll += 0.06 * height
                elif event.y == -1 and lowest_value - height > 0:  # scroll down
                    if (lowest_value - height) < (0.06 * height):
                        y_scroll = (-lowest_value_first)
                    else:
                        y_scroll -= 0.06 * height
            if event.type == pg.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # to cancel
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # to quit game
                quit()
            elif event.type == pygame.MOUSEMOTION or event.type == pygame.KEYDOWN:
                joystick.active = False
                cursor.active = True

        # controller
        joystick.update()

        if joystick.active:
            cursor.active = False

            action = joystick.menu_control(1, buttons_num)
            if action == 'exit' or action == 'enter':
                sound.set_volume(sound_volume * GameSetup.effects_volume)
                pygame.mixer.Channel(1).play(sound)
                return

            if y_scroll <= 0 < lowest_value - height:  # scroll up or down
                if abs(joystick.left_joystick[1]) > 0.2:
                    increment = 0.02 * height * joystick.left_joystick[1]
                else:
                    increment = 0
                y_scroll -= increment
                if y_scroll > 0:
                    y_scroll = 0
                elif y_scroll < -lowest_value_first:
                    y_scroll = -lowest_value_first

        else:
            # cursor
            cursor.active = True
            update_groups([cursor_group], screen)

        clock.tick(GameSetup.fps)
        pygame.display.flip()
