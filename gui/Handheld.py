import sys
from os import getcwd

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QSize, Qt
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
        self.setFixedSize(800, 450)             #Size of the window
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
        # centers widgets
        central_widget = QWidget(self) # creates a widget
        self.setCentralWidget(central_widget) # centers the widget


        # Main vertical layout (two horizontal layouts inside)
        main_layout = QVBoxLayout(central_widget)  # Vertical layout for stacking two rows of buttons

        # upper buttons setup
        upper_layout = QHBoxLayout()
        upper_layout.setContentsMargins(0, 120, 0, 0) #sets spaces between widgets(left, top, right, bottom)
        upper_layout.setSpacing(0)

        # lower buttons setup
        # Scroll area for the slider
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Ensures horizontal scrolling
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   # Disable vertical scrolling

        # Set transparent background for scroll area
        scroll_area.setStyleSheet("background-color: transparent; border: none;")

        scroll_widget = QWidget()  # Widget to hold the icons
        scroll_widget.setStyleSheet("background-color: transparent;")  # Make scroll widget transparent

        scroll_widget = QWidget()  # Widget to hold the icons
        scroll_area.setWidget(scroll_widget)

        lower_layout = QHBoxLayout(scroll_widget)  #sets all self.(QWidget) widgets horizontally and every child of the class QWidget
                                                    #widget1   widget2   widget3# widgets can be buttons in form of picture or whatever
        lower_layout.setContentsMargins(0, 0, 0, 225) #sets spaces between widgets(left, top, right, bottom)
                                                                        #100px
                                                        # 50px widget1   widget2   widget3 50px #
                                                                        #50px

        lower_layout.setSpacing(0)  #widget1 20px widget2 20px widget3#

        # adding both lower and upper buttons to main_layout (order matters)
        main_layout.addLayout(upper_layout)
        main_layout.addWidget(scroll_area)

        # List of menu icons
        self.lower_layout_icons = ['icons/SpaceShooterIcon.png',
                      'icons/cube.png',
                      'icons/reconstruction.png',
                      'icons/reconstruction.png']  #paths to pictures used as buttons later in the code
        # List of small buttons (icons)
        self.upper_layout_icons = ['icons/code.png',
                            'icons/reconstruction.png',
                            'icons/reconstruction.png']  # Paths for small buttons

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

        # Connecting icons to game.exe files with index i = specific number of every picture(button)
        for i, icon in enumerate(self.lower_layout_icons):
            btn = QPushButton(self) #creates a button
            btn.setIcon(QIcon(icon)) #sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(64, 64)) #scales the picture
            btn.setFixedSize(100, 100) #width and height of the button
            btn.setStyleSheet("border: none; background-color: blue;")

            btn.clicked.connect(lambda _, idx=i: self.on_game_item_clicked(idx)) #activating the on menu item clicked function

            self.buttons.append(btn) #adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_hover_leave(b)

            # adding button to lower layout widget list
            lower_layout.addWidget(btn)

        for i, icon in enumerate(self.upper_layout_icons):
            btn = QPushButton(self)  # creates a button
            btn.setIcon(QIcon(icon))  # sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(30, 30))  # scales the picture
            btn.setFixedSize(50, 50)  # width and height of the button
            btn.setStyleSheet("border: none; background-color: red;")

            btn.clicked.connect(
                lambda _, idx=i: self.on_menu_item_clicked(idx))  # activating the on menu item clicked function

            self.buttons.append(btn)  # adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_small_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_small_hover_leave(b)

            # adding button to upper layout widget list
            upper_layout.addWidget(btn)
    # On click event

    def on_game_item_clicked(self, idx):
        game_path = self.games[idx]  # initialise index of the game
        try:
            self.enum = 1
            print(self.enum)
            os.chdir(os.path.dirname(game_path))
            subprocess.run(["python", os.path.basename(game_path)])
            os.chdir(self.gui_path)
            self.enum = 0
            print(self.enum)
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

    # Entry animation on hover

    def on_hover_enter(self, button):
        button.setIconSize(QSize(80, 80))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # Highlights the button

    # Leave animation on hover

    def on_hover_leave(self, button):
        button.setIconSize(QSize(64, 64))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # Reverts the highlight

    def on_small_hover_enter(self, button):
        button.setIconSize(QSize(50, 50))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # Highlights the button

        # Leave animation on hover

    def on_small_hover_leave(self, button):
        button.setIconSize(QSize(30, 30))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # Reverts the highlight

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

