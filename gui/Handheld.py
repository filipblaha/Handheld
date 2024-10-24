import sys
from os import getcwd

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QSize
import subprocess
import os

class HandheldMenu(QMainWindow): # creates class with QMainWindow being its mother code
    def __init__(self):
        super().__init__()

        # Window settings
        self.setFixedSize(800, 450)             #Size of the window
        self.setWindowTitle('Handheld menu')    #Title of the window
        self.setGeometry(100, 100, 800, 400)    #First number = position of window in ur screen(pixels from left)
                                                #Second number = position of window in ur screen(pixels from top)
                                                #Third number = position of window in ur screen(pixels from right)
                                                #Forth number = position of window in ur screen(pixels from bottom)
        self.pixmap = QPixmap('../games/SpaceShooter/game_files/assets/animations/background/Background1.png')
                                                            #sets color of background background-color: #1e1e1e;
                                                            #for custom background picture background-color: => background-image:
                                                            #we can modify the picture here(position, repeating, ...)
        # centers widgets
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)


        # Main vertical layout (two horizontal layouts inside)
        main_layout = QVBoxLayout(central_widget)  # Vertical layout for stacking two rows of buttons

        # lower buttons setup
        lower_layout = QHBoxLayout()  #sets all self.(QWidget) widgets horizontally and every child of the class QWidget
                                                    #widget1   widget2   widget3# widgets can be buttons in form of picture or whatever
        lower_layout.setContentsMargins(50, 30, 50, 50) #sets spaces between widgets(left, top, right, bottom)
                                                                        #100px
                                                        # 50px widget1   widget2   widget3 50px #
                                                                        #50px
        lower_layout.setSpacing(20)  #widget1 20px widget2 20px widget3#

        # upper buttons setup
        upper_layout = QHBoxLayout()
        upper_layout.setContentsMargins(50, 30, 50, 0)
        upper_layout.setSpacing(15)

        # adding both lower and upper buttons to main_layout
        main_layout.addLayout(upper_layout)
        main_layout.addLayout(lower_layout)

        # List of menu icons
        self.icons = ['icons/SpaceShooterIcon.png',
                      'icons/cube.png',
                      'icons/reconstruction.png',
                      'icons/reconstruction.png']  #paths to pictures used as buttons later in the code
        # List of small buttons (icons)
        self.small_icons = ['icons/code.png',
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
        for i, icon in enumerate(self.icons):
            btn = QPushButton(self) #creates a button
            btn.setIcon(QIcon(icon)) #sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(64, 64)) #scales the picture
            btn.setFixedSize(100, 100) #width and height of the button
            btn.setStyleSheet("border: none; background-color: transparent;")

            btn.clicked.connect(lambda _, idx=i: self.on_game_menu_item_clicked(idx)) #activating the on menu item clicked function

            self.buttons.append(btn) #adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_hover_leave(b)

            # adding button to lower layout widget list
            lower_layout.addWidget(btn)

        for i, icon in enumerate(self.small_icons):
            btn = QPushButton(self)  # creates a button
            btn.setIcon(QIcon(icon))  # sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(30, 30))  # scales the picture
            btn.setFixedSize(50, 50)  # width and height of the button
            btn.setStyleSheet("border: none; background-color: transparent;")

            btn.clicked.connect(
                lambda _, idx=i: self.on_game_menu_item_clicked(idx))  # activating the on menu item clicked function

            self.buttons.append(btn)  # adds button to self.buttons list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_small_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_small_hover_leave(b)

            # adding button to upper layout widget list
            upper_layout.addWidget(btn)
    # On click event

    def on_game_menu_item_clicked(self, idx):
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

