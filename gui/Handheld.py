import sys
from os import getcwd
from tkinter import XView

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QScrollArea, QDialog, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QTouchEvent, QMouseEvent, QFont, QFontDatabase, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QSize, Qt, QEvent, QUrl, QTimer
import pygame
import subprocess
import os

# Here’s how the layers work together in a PyQt5 application:
#
# Application Layer: Initializes and runs the application.
# Main Window Layer: Sets up the main window and frame for the app.
# Central Widget Layer: Holds the main content within the main window.
# Layout Layer: Organizes widgets within the central widget.
# Widget Layer: Contains interactive components like buttons, labels, and inputs.
# Event Handling and Signal-Slot Layer: Connects user actions with the application’s responses.
# Custom Classes and Logic Layer: Defines custom widgets, data, or other functionalities.
# Styling Layer: (Optional) Customizes the look of the application.

class HandheldMenu(QMainWindow): # creates class with QMainWindow being its mother code
    def __init__(self):
        super().__init__()

        # Window settings
        self.window_width = 800
        self.window_height = 450
        self.setFixedSize(self.window_width, self.window_height)             #Size of the window
        self.setWindowTitle('Handheld menu')    #Title of the window
        #self.setWindowFlags(Qt.FramelessWindowHint) # Hides all outlines and top bar of window

        self.setGeometry(0, 0, 0, 0)            #First number = position of window in ur screen(pixels from left)
                                                #Second number = position of window in ur screen(pixels from top)
                                                #Third number = position of window in ur screen(pixels from right)
                                                #Forth number = position of window in ur screen(pixels from bottom)
        # Path to the gui(from this file we navigate to the game/gui files)
        self.gui_path = getcwd()

        self.pixmap = QPixmap('../gui/icons/Background.png') # sets background pic

        # Background music setup (is supposed to play all the time in the background in a menu)
        self.background_music = QMediaPlayer()
        self.background_music_path = os.path.join(self.gui_path, 'audio/background_retro_game_music.mp3')
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile(self.background_music_path)))
        self.background_music.setVolume(50)  # Base audio volume is 50
        self.background_music.play()  # Automatically starts the audio
        # Connect mediaStatusChanged signal
        self.background_music.mediaStatusChanged.connect(self.handle_music_status)

        # Button audio (is supposed to play when someone hovers a button)
        self.button_sound = QMediaPlayer()
        self.button_sound_path = os.path.join(self.gui_path, 'audio/button_short.mp3')
        self.button_sound.setMedia(QMediaContent(QUrl.fromLocalFile(self.button_sound_path)))
        self.button_sound.setVolume(50)  # Base audio volume is 50

        # Controller settings prep
        self.typeof_volume = "button"
        self.button_volume_value = 0
        self.background_volume_value = 0
        self.volume_slider = 0

        # code enabling to be controlled by touch (touch screen support)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        # centers widgets
        central_widget = QWidget(self) # creates a widget
        self.setCentralWidget(central_widget) # centers the widget


        # Main vertical layout (two horizontal layouts inside)
        main_layout = QVBoxLayout(central_widget)  # Vertical layout for stacking two rows of buttons

        # lower buttons setup
        # Scroll area for the slider
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Ensures horizontal scrolling
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   # Disable vertical scrolling


        # changes swipe action to scroll in scroll_area
        scroll_area.grabGesture(Qt.PanGesture)

        # Set transparent background for scroll area
        scroll_area.setStyleSheet("background-color: transparent; border: none;")

        scroll_widget = QWidget()  # Widget to hold the icons
        scroll_widget.setStyleSheet("background-color: transparent;")  # Make scroll widget transparent

        scroll_widget = QWidget()  # Widget to hold the icons
        scroll_area.setWidget(scroll_widget)

        lower_layout = QHBoxLayout(scroll_widget)  #sets all self.(QWidget) widgets horizontally and every child of the class QWidget
                                                    #widget1   widget2   widget3# widgets can be buttons in form of picture or whatever
        # upper layout creation
        upper_layout = QHBoxLayout()

        # adding both lower and upper buttons to main_layout (order matters)
        main_layout.addLayout(upper_layout)
        main_layout.addWidget(scroll_area)

        # List of menu icons
        self.lower_layout_icon = ['icons/SpaceShooterIcon.png',
                      'icons/cube.png']  #paths to pictures used as buttons later in the code
        self.lower_layout_icon_count = len(self.lower_layout_icon) # number of icons in the list of lower layout

        # List of small buttons (icons)
        self.upper_layout_icon = ['/Users/tomasfikart/PycharmProjects/Handheld/gui/icons/settings_button1.png']  # Paths for small buttons
        self.upper_layout_icon_count = len(self.upper_layout_icon)

        # List of games
        self.games = ['../games/SpaceShooter/main.py', '../games/Tester/Handheld_tester.py'] # source of the game .exe (indexes decides which one to start so order matters)

        # List of menu buttons
        self.menu = [self.settings] # starts the code of the menu

        # font setup
        os.chdir(self.gui_path)
        font_path = os.path.join(self.gui_path,'fonts/upheaval/upheavtt.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Font se nepodařilo načíst!")
        else:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                print("Font se načetl správně:", families)
            else:
                print("Font neobsahuje žádné rodiny!")
        os.chdir(self.gui_path)
        # enum = number which represents state of the code (menu = 0, game = 1, menu_settings = 2)
        self.enum = 0

        # Store buttons for easy access
        self.buttons = [] #list of all QPushButton(adding all buttons to this list)

        # lower button mathing (scaling)
        self.lower_button_spacing = int(self.window_width/13.33333)
        self.lower_button_width = int(self.window_width / 8)
        self.lower_button_height = int(self.window_height / 4.8)
        self.lower_button_icon_width = int(self.window_width / 12.5)
        self.lower_button_icon_height = int(self.window_height / 7.03125)
        self.lower_button_top_limit = int((2/6)*self.window_height)
        self.lower_button_left_limit = int((self.window_width - (self.lower_button_width * self.lower_layout_icon_count +
                                                             self.lower_button_spacing * (self.lower_layout_icon_count-1)))/2)
        self.lower_button_right_limit = int((self.window_width - (self.lower_button_width * self.lower_layout_icon_count +
                                                             self.lower_button_spacing * (self.lower_layout_icon_count-1)))/2)
        self.lower_button_bottom_limit = int((2/6)*self.window_height)

        # lower layout setup
        lower_layout.setContentsMargins(self.lower_button_left_limit, 0, self.lower_button_right_limit, self.lower_button_bottom_limit)
                                                #sets spaces between widgets(left, top, right, bottom)
                                                                        #100px
                                                        # 50px widget1   widget2   widget3 50px #
                                                                        #50px
        lower_layout.addStretch(1)
        lower_layout.setSpacing(self.lower_button_spacing)  #widget1 20px widget2 20px widget3#

        # Connecting icons to game.exe files with index i = specific number of every picture(button)
        for i, icon in enumerate(self.lower_layout_icon):
            btn = QPushButton(self) #creates a button
            btn.setIcon(QIcon(icon)) #sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(self.lower_button_icon_width, self.lower_button_icon_height)) #scales the picture
            btn.setFixedSize(self.lower_button_width, self.lower_button_height) #width and height of the button
            btn.setStyleSheet("border: none; background-color: transparent;")

            btn.clicked.connect(lambda _, idx=i: self.on_game_item_clicked(idx)) #activating the on menu item clicked function

            self.buttons.append(btn) #adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_lower_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_lower_hover_leave(b)

            # adding button to lower layout widget list
            lower_layout.addWidget(btn)

        # upper buttons mathing (scaling)
        self.upper_button_spacing = int(self.window_width / 26.666666) # could have used double slash // to round the number to integer
        self.upper_button_width = int(self.window_width / 16)
        self.upper_button_height = int(self.window_height / 9.6)
        self.upper_button_icon_width = int(self.window_width / 26.666666)
        self.upper_button_icon_height = int(self.window_height / 15)
        self.upper_button_left_limit = int((self.window_width - (self.upper_button_width * self.upper_layout_icon_count +
                                                             self.upper_button_spacing * (self.upper_layout_icon_count-1)))/2)
        self.upper_button_top_limit = int((1/5)*self.window_height)
        self.upper_button_right_limit = int((self.window_width - (self.upper_button_width * self.upper_layout_icon_count +
                                                             self.upper_button_spacing * (self.upper_layout_icon_count-1)))/2)
        self.upper_button_bottom_limit = int((2/6)*self.window_height)

        # upper buttons setup
        upper_layout.addStretch(1)
        upper_layout.setContentsMargins(self.upper_button_left_limit,   self.upper_button_top_limit,
                                        self.upper_button_right_limit,0) #sets spaces between widgets(left, top, right, bottom)
        upper_layout.setSpacing(self.upper_button_spacing)

        for i, icon in enumerate(self.upper_layout_icon):
            btn = QPushButton(self)  # creates a button
            btn.setIcon(QIcon(icon))  # sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(self.upper_button_icon_width, self.upper_button_icon_height))  # scales the picture
            btn.setFixedSize(self.upper_button_width, self.upper_button_height)  # width and height of the button
            btn.setStyleSheet("border: none; background-color: transparent;")

            btn.clicked.connect(lambda _, idx=i: self.on_menu_item_clicked(idx))  # activating the on menu item clicked function

            self.buttons.append(btn)  # adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_upper_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_upper_hover_leave(b)

            # adding button to upper layout widget list
            upper_layout.addWidget(btn)

        # Controller setup
        pygame.init()
        pygame.joystick.init()
        self.controller = None
        self.current_button_index = 0
        self.last_move_time = 0

        # Controller input timer
        self.controller_timer = QTimer(self)
        self.controller_timer.timeout.connect(self.check_controller_input)
        self.controller_timer.start(50)  # Check every 50ms

        # Initialize pygame for controller support
        self.pygame_initialized = False
        self.init_pygame()

    def handle_music_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.background_music.play()  # Restart the music

    def init_pygame(self):
        """Initialize pygame only for controller support"""
        try:
            pygame.init()
            pygame.joystick.init()
            self.pygame_initialized = True
            print("Pygame initialized for controller support")
        except Exception as e:
            print(f"Error initializing pygame: {e}")
            self.pygame_initialized = False

    def setup_controller(self):
            """Initialize the controller if connected"""
            if not self.pygame_initialized:
                self.init_pygame()
                if not self.pygame_initialized:
                    return None

            try:
                pygame.joystick.quit()  # Clean up first
                pygame.joystick.init()

                joystick_count = pygame.joystick.get_count()
                if joystick_count > 0:
                    controller = pygame.joystick.Joystick(0)
                    controller.init()
                    print(f"Controller detected: {controller.get_name()}")
                    return controller
            except Exception as e:
                print(f"Controller init error: {e}")
            return None

    def check_controller_input(self):
            """Check for controller input and handle navigation"""
            if not hasattr(self, 'controller') or self.controller is None:
                self.controller = self.setup_controller()
                if self.controller is None:
                    return

            try:
                # Process pygame events to keep the queue clear
                for event in pygame.event.get():
                    pass

                # control
                # joysticks
                self.left_joystick = (self.controller.get_axis(0), self.controller.get_axis(1))
                self.right_joystick = (self.controller.get_axis(2), self.controller.get_axis(3))

                # L2/R2
                self.L2 = self.controller.get_axis(4)
                self.R2 = self.controller.get_axis(5)

                # buttons
                self.cross_button = self.controller.get_button(0)
                self.circle_button = self.controller.get_button(1)
                self.square_button = self.controller.get_button(2)
                self.triangle_button = self.controller.get_button(3)
                self.options_button = self.controller.get_button(6)
                self.L1 = self.controller.get_button(9)
                self.R1 = self.controller.get_button(10)
                self.arrow_up = self.controller.get_button(11)
                self.arrow_down = self.controller.get_button(12)
                self.arrow_left = self.controller.get_button(13)
                self.arrow_right = self.controller.get_button(14)

                # Apply deadzones
                self.apply_deadzone(self.right_joystick[0]),self.apply_deadzone(self.right_joystick[1])
                self.apply_deadzone(self.left_joystick[0]),self.apply_deadzone(self.left_joystick[1])

                # Navigation with left stick
                move_threshold = 0.5
                move_delay = 200 # ms
                current_time = pygame.time.get_ticks()

            except Exception as e:
                print(f"Controller input error: {e}")

            if self.enum == 0:
                if current_time - self.last_move_time > move_delay:
                    moved = False

                    # Left navigation
                    if self.left_joystick[0] < -move_threshold or self.arrow_left == True:
                        self.navigate_buttons(-1)
                        moved = True
                    # Right navigation
                    elif self.left_joystick[0] > move_threshold or self.arrow_right == True:
                        self.navigate_buttons(1)
                        moved = True
                    # Up navigation
                    if self.left_joystick[1] < -move_threshold or self.arrow_up == True:
                        self.navigate_vertical(-1)
                        moved = True
                    # Down navigation
                    elif self.left_joystick[1] > move_threshold or self.arrow_down == True:
                        self.navigate_vertical(1)
                        moved = True

                    if moved:
                        self.last_move_time = current_time
                        self.button_sound.play()

                # Button presses
                if self.cross_button:  # X button for selection (PS4 button mapping)
                    self.buttons[self.current_button_index].click()
                if self.options_button:
                    self.on_menu_item_clicked(0)

            if self.enum == 2:
                if current_time - self.last_move_time > move_delay:
                    moved = False
                    #Joystick up
                    if self.left_joystick[1] < -move_threshold or self.arrow_up == True:
                        self.typeof_volume = "button"
                        moved = True

                    #Joystick down
                    elif self.left_joystick[1] > move_threshold or self.arrow_down == True:
                        self.typeof_volume = "background"
                        moved = True

                    # Změna hlasitosti podle typu

                    #Joystick left
                    if self.left_joystick[0] < -move_threshold or self.arrow_left == True:
                        if self.typeof_volume == "button":
                            new_value = max(0, self.button_volume_slider.value() - 5)
                            self.button_volume_slider.setValue(new_value)
                        else:
                            new_value = max(0, self.background_volume_slider.value() - 5)
                            self.background_volume_slider.setValue(new_value)
                        moved = True

                    #Joystick right
                    elif self.left_joystick[0] > move_threshold or self.arrow_right == True:
                        if self.typeof_volume == "button":
                            new_value = min(100, self.button_volume_slider.value() + 5)
                            self.button_volume_slider.setValue(new_value)
                        else:
                            new_value = min(100, self.background_volume_slider.value() + 5)
                            self.background_volume_slider.setValue(new_value)
                        moved = True

                    if moved:
                        self.last_move_time = current_time

                if self.circle_button:
                    self.back_button.click()


    def apply_deadzone(self, value, deadzone=0.2):
        """Apply deadzone to analog stick values"""
        if abs(value) < deadzone:
            return 0
        return value

    def navigate_buttons(self, direction):
        """Navigate horizontally between buttons"""
        if not self.buttons:
            return

        # Remove highlight from current button
        self.highlight_current_button(False)

        # Calculate new index
        self.current_button_index += direction
        if self.current_button_index < 0:
            self.current_button_index = len(self.buttons) - 1
        elif self.current_button_index >= len(self.buttons):
            self.current_button_index = 0

        # Highlight new button
        self.highlight_current_button(True)

    def navigate_vertical(self, direction):
        """Navigate vertically between button rows with custom buttons per row"""
        if not self.buttons:
            return

        # Předdefinované rozložení řádků (např. [2, 2])
        rows_layout = [self.lower_layout_icon_count, self.upper_layout_icon_count]  # Upravte podle vašich potřeb

        # Najděte aktuální řádek a sloupec
        current_row = 0
        remaining_index = self.current_button_index
        for i, buttons_in_row in enumerate(rows_layout):
            if remaining_index < buttons_in_row:
                current_row = i
                current_col = remaining_index
                break
            remaining_index -= buttons_in_row
        else:
            current_row = len(rows_layout) - 1
            current_col = rows_layout[-1] - 1  # Poslední tlačítko v posledním řádku

        # Vypočtěte nový řádek
        new_row = current_row + direction
        total_rows = len(rows_layout)

        if new_row < 0:
            new_row = total_rows - 1  # Přetečení nahoru → poslední řádek
        elif new_row >= total_rows:
            new_row = 0  # Přetečení dolů → první řádek

        # Omezení sloupce, pokud nový řádek má méně tlačítek
        new_col = min(current_col, rows_layout[new_row] - 1)

        # Vypočtěte nový index
        new_index = sum(rows_layout[:new_row]) + new_col

        # Aktualizace zvýraznění
        self.highlight_current_button(False)
        self.current_button_index = new_index
        self.highlight_current_button(True)

    def highlight_current_button(self, highlight):
        """Use existing hover animations for controller navigation"""
        if hasattr(self, 'current_button_index') and self.buttons and 0 <= self.current_button_index < len(
                self.buttons):
            button = self.buttons[self.current_button_index]
            if highlight:
                # Use the same effect as hover enter
                if self.current_button_index < len(self.lower_layout_icon):
                    button.setIconSize(
                        QSize(int(self.lower_button_icon_width * 1.2), int(self.lower_button_icon_height * 1.2)))
                else:
                    button.setIconSize(
                        QSize(int(self.upper_button_icon_width * 1.2), int(self.upper_button_icon_height * 1.2)))
                self.button_sound.play()
            else:
                # Use the same effect as hover leave
                if self.current_button_index < len(self.lower_layout_icon):
                    button.setIconSize(QSize(self.lower_button_icon_width, self.lower_button_icon_height))
                else:
                    button.setIconSize(QSize(self.upper_button_icon_width, self.upper_button_icon_height))

    def on_game_item_clicked(self, idx):
        game_path = self.games[idx]  # initialise index of the game
        try:
            self.enum = 1
            self.background_music_controller()
            os.chdir(os.path.dirname(game_path))
            subprocess.run(["python3", os.path.basename(game_path)])
            os.chdir(self.gui_path)
            self.enum = 0
            self.background_music_controller()
        except Exception as e: # in case of error
            print(f"Chyba při spuštění hry: {e}")

    def on_menu_item_clicked(self, idx):
        menu_action = self.menu[idx]  # initialise index of the game
        try:
            if callable(menu_action):
                self.enum =2
                menu_action()
            else:
                self.enum = 2
                self.background_music_controller()
                os.chdir(os.path.dirname(menu_action))                      #os.path.dirname = everything except the last part of the path to the file
                subprocess.run(["python3", os.path.basename(menu_action)])   #os.path.basename = last part of file path
                os.chdir(self.gui_path)
                self.enum = 0
                self.background_music_controller()
        except Exception as e: # in case of error
            print(f"Chyba při spuštění menu: {e}")

    # Entry animation on hover
    def on_lower_hover_enter(self, button):
        button.setIconSize(QSize(int(self.lower_button_icon_width*1.2), int(self.lower_button_icon_height*1.2)))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # options to change background
        self.button_sound.play()

    # Leave animation on hover
    def on_lower_hover_leave(self, button):
        button.setIconSize(QSize(self.lower_button_icon_width, self.lower_button_icon_height))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # options to change background

    def on_upper_hover_enter(self, button):
        button.setIconSize(QSize(int(self.upper_button_icon_width*1.2), int(self.upper_button_icon_height*1.2)))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # options to change background
        self.button_sound.play()

    # Leave animation on hover
    def on_upper_hover_leave(self, button):
        button.setIconSize(QSize(self.upper_button_icon_width, self.upper_button_icon_height))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # options to change background

    # defining actions performed by style of touch (touch screen support)
    def touchEvent(self, event: QTouchEvent):
        for touch_point in event.touchPoints():
            # performs this code on press of finger
            if touch_point.state() == Qt.TouchPointPressed:
                mouse_event_press = QMouseEvent(QEvent.Type.MouseButtonPress, touch_point.pos(), Qt.LeftButton,
                                                Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self, mouse_event_press)
            # performs this code on release of finger
            elif touch_point.state() == Qt.TouchPointReleased:
                mouse_event_release = QMouseEvent(QEvent.Type.MouseButtonRelease, touch_point.pos(), Qt.LeftButton,
                                                  Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self, mouse_event_release)
            # scrolling through is coded somewhere else cause its easier
        event.accept()  # Mark the event as handled

    # Method for painting the background
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw the background image
        scaled_pixmap = self.pixmap.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_pixmap)

    # settings function
    def settings(self):
        # Hide main menu buttons
        for button in self.buttons:
            button.hide()

        self.settings_widgets = []

        # Set font for labels
        self.font = QFont('Upheaval TT (BRK)', 18, QFont.Bold)

        # Create labels for the sliders
        self.button_volume_label = QLabel("Button Volume", self)
        self.button_volume_label.setFont(self.font)
        self.button_volume_label.adjustSize()
        self.background_volume_label = QLabel("Background Volume", self)
        self.background_volume_label.setFont(self.font)
        self.background_volume_label.adjustSize()

        # Create sliders for button and background sound volumes
        self.button_volume_slider = QSlider(Qt.Horizontal, self)
        self.button_volume_slider.setRange(0, 100)
        self.button_volume_slider.setValue(50)
        self.button_volume_slider.valueChanged.connect(self.update_button_volume)
        self.button_volume_slider.setFixedWidth(200)

        self.background_volume_slider = QSlider(Qt.Horizontal, self)
        self.background_volume_slider.setRange(0, 100)
        self.background_volume_slider.setValue(50)
        self.background_volume_slider.valueChanged.connect(self.update_background_volume)
        self.background_volume_slider.setFixedWidth(200)
        # Calculate centered positions based on window size
        center_x = self.window_width // 2
        center_y = self.window_height // 2

        # Position the labels and sliders centrally
        self.button_volume_label.move(center_x - 75, center_y - 80)
        self.button_volume_slider.move(center_x - 75, center_y - 50)
        self.background_volume_label.move(center_x - 75, center_y + 10)
        self.background_volume_slider.move(center_x - 75, center_y + 40)

        # Create "Back to Menu" button
        self.back_button = QPushButton("Back to Menu", self)
        self.back_button.setStyleSheet("background-color: #333; color: white; border: none;")
        self.back_button.setFont(self.font)
        self.back_button.setFixedSize(160, 40)
        self.back_button.move(self.window_width - self.back_button.width() - 10, 10)  # Position in top-right corner
        self.back_button.clicked.connect(self.show_main_menu)
        self.back_button.show()

        #adding everything to the list of the settings_widgets
        self.settings_widgets.append(self.button_volume_label)
        self.settings_widgets.append(self.button_volume_slider)
        self.settings_widgets.append(self.background_volume_label)
        self.settings_widgets.append(self.background_volume_slider)
        self.settings_widgets.append(self.back_button)

        #shows all the self.settings_widgets
        for setting_widget in self.settings_widgets:
            setting_widget.show()

        self.button_volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #5c5c5c;
                width: 18px;
                height: 18px;
                margin: -5px 0;  /* Center handle */
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #e0e0e0;
                border-radius: 4px;
            }
        """)

        self.background_volume_slider.setStyleSheet(self.button_volume_slider.styleSheet())

    # Function to show the main menu and hide settings
    def show_main_menu(self):
        # hides all settings widgets
        for widget in self.settings_widgets:
            widget.hide()

        # Show all main menu buttons
        for button in self.buttons:
            button.show()
        self.enum = 0


    # Volume update methods for sliders
    def update_button_volume(self, value):
        print(f"Button volume set to: {value}")
        self.button_sound.setVolume(value)

    def update_background_volume(self, value):
        self.background_music.setVolume(value)
        print(f"Background volume set to: {value}")

    def background_music_controller(self):
        if self.enum == 0:  # Menu
            self.background_music.play()
            # Re-enable controller if it was disabled
            if self.controller and not self.controller.get_init():
                self.controller.init()
        elif self.enum == 1:  # Game
            self.background_music.stop()
            # Disable controller for game
            if self.controller and self.controller.get_init():
                self.controller.quit()
        elif self.enum == 2:  # Settings
            self.background_music.play()
            # Ensure controller is enabled for settings
            if self.controller and not self.controller.get_init():
                self.controller.init()

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandheldMenu()
    window.show()
    sys.exit(app.exec_())

