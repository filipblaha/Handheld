import sys
from os import getcwd

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QTouchEvent, QMouseEvent
from PyQt5.QtCore import QSize, Qt, QEvent
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
        self.setGeometry(350, 200, 200, 200)    #First number = position of window in ur screen(pixels from left)
                                                #Second number = position of window in ur screen(pixels from top)
                                                #Third number = position of window in ur screen(pixels from right)
                                                #Forth number = position of window in ur screen(pixels from bottom)

        self.pixmap = QPixmap('../games/SpaceShooter/game_files/assets/animations/background/Background1.png')
                                                            #sets color of background background-color: #1e1e1e;
                                                            #for custom background picture background-color: => background-image:
                                                            #we can modify the picture here(position, repeating, ...)

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
                      'icons/cube.png',
                      'icons/reconstruction.png',
                      'icons/reconstruction.png']  #paths to pictures used as buttons later in the code
        self.lower_layout_icon_count = len(self.lower_layout_icon) # nuumber of icons in the list of lower layout

        # List of small buttons (icons)
        self.upper_layout_icon = ['icons/code.png',
                            'icons/reconstruction.png',
                            'icons/reconstruction.png']  # Paths for small buttons
        self.upper_layout_icon_count = len(self.upper_layout_icon)

        # List of games
        self.games = ['../games/SpaceShooter/game_files/main.py', '../games/Tester/Handheld_tester.py', '',''] # source of the game .exe (indexes decides which one to start so order matters)

        # List of menu buttons
        self.menu = ['../gui/Handheld.py','',''] # starts the code of the menu

        # Path to the gui(from this file we navigate to the game/gui files)
        self.gui_path = getcwd()

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
        self.upper_button_spacing = int(self.window_width/26.666666)
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
    # On click event

    def on_game_item_clicked(self, idx):
        game_path = self.games[idx]  # initialise index of the game
        try:
            self.enum = 1
            os.chdir(os.path.dirname(game_path))
            subprocess.run(["python", os.path.basename(game_path)])
            os.chdir(self.gui_path)
            self.enum = 0
        except Exception as e: # in case of error
            print(f"Chyba při spuštění hry: {e}")

    def on_menu_item_clicked(self, idx):
        menu_action = self.menu[idx]  # initialise index of the game
        try:
            self.enum = 2
            os.chdir(os.path.dirname(menu_action))                      #os.path.dirname = everything except the last part of the path to the file
            subprocess.run(["python", os.path.basename(menu_action)])   #os.path.basename = last part of file path
            os.chdir(self.gui_path)
            self.enum = 0
        except Exception as e: # in case of error
            print(f"Chyba při spuštění menu: {e}")

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

    # Entry animation on hover
    def on_lower_hover_enter(self, button):
        button.setIconSize(QSize(int(self.lower_button_icon_width*1.2), int(self.lower_button_height*1.2)))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # options to change background

    # Leave animation on hover
    def on_lower_hover_leave(self, button):
        button.setIconSize(QSize(self.lower_button_icon_width, self.lower_button_height))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # options to change background

    def on_upper_hover_enter(self, button):
        button.setIconSize(QSize(int(self.upper_button_icon_width*1.2), int(self.upper_button_icon_height*1.2)))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # options to change background

    # Leave animation on hover
    def on_upper_hover_leave(self, button):
        button.setIconSize(QSize(self.upper_button_icon_width, self.upper_button_icon_height))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # options to change background

    # Method for painting the background
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw the background image
        scaled_pixmap = self.pixmap.scaled(self.size(), aspectRatioMode=1)
        painter.drawPixmap(0, 0, scaled_pixmap)

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandheldMenu()
    window.show()
    sys.exit(app.exec_())

