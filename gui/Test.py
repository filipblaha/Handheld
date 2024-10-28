import sys
from os import getcwd
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QGridLayout,
QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QSize, Qt
import subprocess
import os

class HandheldMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setFixedSize(800, 450)
        self.setWindowTitle('Handheld menu')
        self.setGeometry(100, 100, 800, 400)

        self.pixmap = QPixmap('../games/SpaceShooter/game_files/assets/animations/background/Background1.png')

        # Main vertical layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Set up grid layout as main layout
        main_layout = QVBoxLayout(central_widget)

        # Add a spacer above the upper layout to push it down slightly
        # Upper layout
        upper_widget = QWidget()
        upper_layout = QHBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 30, 0, 0)  # Move upper layout higher
        upper_layout.setSpacing(5)

        # Lower layout
        lower_widget = QWidget()
        lower_layout = QHBoxLayout(lower_widget)
        lower_layout.setContentsMargins(0, 100, 0, 0)  # Center lower layout
        lower_layout.setSpacing(60)

        # Spacer to push the upper layout down a bit
        main_layout.addSpacerItem(QSpacerItem(500, 5000, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add upper layout to main_layout, aligned at the top
        main_layout.addWidget(upper_widget, alignment=Qt.AlignTop)

        # Spacer to control space between upper and lower layouts
        main_layout.addSpacerItem(QSpacerItem(0, 10000, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add lower layout to main_layout, aligned to the center
        main_layout.addWidget(lower_widget, alignment=Qt.AlignHCenter | Qt.AlignTop)

        # Spacer to push the lower layout slightly up from the bottom
        main_layout.addSpacerItem(QSpacerItem(0, 50000, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Icons and buttons setup (same as your original code)
        self.lower_layout_icons = ['icons/SpaceShooterIcon.png',
                                   'icons/cube.png',
                                   'icons/reconstruction.png',
                                   'icons/reconstruction.png']
        self.upper_layout_icons = ['icons/code.png',
                                   'icons/reconstruction.png',
                                   'icons/reconstruction.png']

        self.games = ['../games/SpaceShooter/game_files/main.py', '../games/Tester/Handheld_tester.py', '','']
        self.menu = ['../gui/Handheld.py','','']

        self.gui_path = getcwd()
        self.enum = 0
        self.buttons = []

        # Create buttons for lower layout
        for i, icon in enumerate(self.lower_layout_icons):
            btn = QPushButton(self)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(64, 64))
            btn.setFixedSize(100, 100)
            btn.setStyleSheet("border: none; background-color: transparent;")
            btn.clicked.connect(lambda _, idx=i: self.on_game_item_clicked(idx))
            self.buttons.append(btn)

            btn.enterEvent = lambda event, b=btn: self.on_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_hover_leave(b)
            lower_layout.addWidget(btn)

        # Create buttons for upper layout
        for i, icon in enumerate(self.upper_layout_icons):
            btn = QPushButton(self)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(30, 30))
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("border: none; background-color: transparent;")
            btn.clicked.connect(lambda _, idx=i: self.on_menu_item_clicked(idx))
            self.buttons.append(btn)

            btn.enterEvent = lambda event, b=btn: self.on_small_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_small_hover_leave(b)
            upper_layout.addWidget(btn)

    def on_game_item_clicked(self, idx):
        game_path = self.games[idx]
        try:
            self.enum = 1
            os.chdir(os.path.dirname(game_path))
            subprocess.run(["python", os.path.basename(game_path)])
            os.chdir(self.gui_path)
            self.enum = 0
        except Exception as e:
            print(f"Chyba při spuštění hry: {e}")

    def on_menu_item_clicked(self, idx):
        menu_action = self.menu[idx]
        try:
            self.enum = 2
            os.chdir(os.path.dirname(menu_action))
            subprocess.run(["python", os.path.basename(menu_action)])
            os.chdir(self.gui_path)
            self.enum = 0
        except Exception as e:
            print(f"Chyba při spuštění menu: {e}")

    def on_hover_enter(self, button):
        button.setIconSize(QSize(80, 80))
        button.setStyleSheet("background-color: transparent;")

    def on_hover_leave(self, button):
        button.setIconSize(QSize(64, 64))
        button.setStyleSheet("background-color: transparent;")

    def on_small_hover_enter(self, button):
        button.setIconSize(QSize(50, 50))
        button.setStyleSheet("background-color: transparent;")

    def on_small_hover_leave(self, button):
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_pixmap = self.pixmap.scaled(self.size(), aspectRatioMode=1)
        painter.drawPixmap(0, 0, scaled_pixmap)

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandheldMenu()
    window.show()
    sys.exit(app.exec_())
