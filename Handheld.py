import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import subprocess


class HandheldMenu(QMainWindow): # creates class with QMainWindow being its mother code
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle('Handheld menu')    #Title of the window
        self.setGeometry(100, 100, 800, 400)    #First number = position of window in ur screen(pixels from left)
                                                #Second number = position of window in ur screen(pixels from top)
                                                #Third number = position of window in ur screen(pixels from right)
                                                #Forth number = position of window in ur screen(pixels from bottom)
        self.setStyleSheet("""
            background-image: url('/Users/tomasfikart/Documents/Handheld/Background/Background1.png');
            background-repeat: no-repeat;
            background-position: center;
        """)    #sets color of background background-color: #1e1e1e;
                                                            #for custom background picture background-color: => background-image:
                                                            #we can modify the picture here(position, repeating, ...)
        # Centres all widgets
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        self.layout = QHBoxLayout(central_widget) #sets all self.(QWidget) widgets horizontally and every child of the class QWidget
                                        #widget1   widget2   widget3# widgets can be buttons in form of picture or whatever
        self.layout.setContentsMargins(50, 100, 50, 50) #sets spaces between widgets(left, top, right, bottom)
                                                                        #100px
                                                        # 50px widget1   widget2   widget3 50px #
                                                                        #50px
        self.layout.setSpacing(20)  #widget1 20px widget2 20px widget3#

        # List of menu items
        self.icons = ['/Users/tomasfikart/Documents/Handheld/Buttons/zarovka.png', '/Users/tomasfikart/Documents/Handheld/Buttons/sniper.png', '/Users/tomasfikart/Documents/Handheld/Buttons/sniper.png', '/Users/tomasfikart/Documents/Handheld/Buttons/settings_button1.png']  #paths to pictures used as buttons later in the code

        # List of games
        self.games = ['path to the game.exe']

        # Store buttons for easy access
        self.buttons = [] #list of all QPushButton(adding all buttons to this list)

        # Connecting icons to game.exe files with index i = specific number of every picture(button)
        for i, icon in enumerate(self.icons):
            btn = QPushButton(self) #creates a button
            btn.setIcon(QIcon(icon)) #sets visuals of the button to picture from icon list
            btn.setIconSize(QSize(64, 64)) #scales the picture
            btn.setFixedSize(100, 100) #width and height of the button
            btn.setStyleSheet("border: none; background-color: transparent;")

            btn.clicked.connect(lambda _, idx=i: self.on_menu_item_clicked(idx)) #activating the on menu item clicked function

            self.buttons.append(btn) #adds button to self.buttons list
            self.layout.addWidget(btn) #moves button to widget list

            # animations of buttons
            btn.enterEvent = lambda event, b=btn: self.on_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_hover_leave(b)

    # On click event

    def on_menu_item_clicked(self, idx):
        game_path = self.games[idx]  # initialise index of the game
        try:
            subprocess.Popen(game_path)  # starts the game file
        except Exception as e: # in case of error
            print(f"Chyba při spuštění hry: {e}")

    # Entry animation on hover

    def on_hover_enter(self, button):
        button.setIconSize(QSize(80, 80))  # Enlarges icon
        button.setStyleSheet("background-color: transparent;")  # Highlights the button

    # Leave animation on hover

    def on_hover_leave(self, button):
        button.setIconSize(QSize(64, 64))  # Reverts the icon to the original size
        button.setStyleSheet("background-color: transparent;")  # Reverts the highlight


# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandheldMenu()
    window.show()
    sys.exit(app.exec_())

