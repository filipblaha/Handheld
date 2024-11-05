import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QTouchEvent, QMouseEvent
from PyQt5.QtCore import QSize, Qt, QEvent
import subprocess
import os


class HandheldMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.window_width = 800
        self.window_height = 450
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle('Handheld menu')

        # Background image
        self.pixmap = QPixmap('../games/SpaceShooter/game_files/assets/animations/background/Background1.png')

        # Touch support
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        # Central widget and layout setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Scroll area for the lower layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        scroll_area.grabGesture(Qt.PanGesture)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: transparent;")
        scroll_area.setWidget(scroll_widget)
        lower_layout = QHBoxLayout(scroll_widget)

        # Upper layout
        upper_layout = QHBoxLayout()

        # Adding layouts to main layout
        main_layout.addLayout(upper_layout)
        main_layout.addWidget(scroll_area)

        # Icons and paths
        self.lower_layout_icon = ['icons/SpaceShooterIcon.png', 'icons/cube.png', 'icons/reconstruction.png',
                                  'icons/reconstruction.png']
        self.upper_layout_icon = ['icons/code.png', 'icons/reconstruction.png', 'icons/reconstruction.png']
        self.games = ['../games/SpaceShooter/game_files/main.py', '../games/Tester/Handheld_tester.py', '', '']

        # Here we add `self.settings` function to menu list so it can be accessed
        self.menu = ['../gui/Handheld.py', self.settings, '']
        self.gui_path = getcwd()
        self.enum = 0
        self.buttons = []

        # Lower button setup
        self.lower_button_spacing = int(self.window_width / 13.33333)
        self.lower_button_width = int(self.window_width / 8)
        self.lower_button_height = int(self.window_height / 4.8)
        self.lower_button_icon_width = int(self.window_width / 12.5)
        self.lower_button_icon_height = int(self.window_height / 7.03125)
        lower_layout.setContentsMargins(self.lower_button_spacing, 0, self.lower_button_spacing,
                                        int(self.window_height / 6))
        lower_layout.addStretch(1)
        lower_layout.setSpacing(self.lower_button_spacing)

        for i, icon in enumerate(self.lower_layout_icon):
            btn = QPushButton(self)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(self.lower_button_icon_width, self.lower_button_icon_height))
            btn.setFixedSize(self.lower_button_width, self.lower_button_height)
            btn.setStyleSheet("border: none; background-color: transparent;")
            btn.clicked.connect(lambda _, idx=i: self.on_game_item_clicked(idx))
            self.buttons.append(btn)
            btn.enterEvent = lambda event, b=btn: self.on_lower_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_lower_hover_leave(b)
            lower_layout.addWidget(btn)

        # Upper button setup
        upper_layout.setContentsMargins(int(self.window_width / 20), int(self.window_height / 5),
                                        int(self.window_width / 20), 0)
        upper_layout.addStretch(1)
        upper_layout.setSpacing(int(self.window_width / 26.666666))

        for i, icon in enumerate(self.upper_layout_icon):
            btn = QPushButton(self)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(int(self.window_width / 26.666666), int(self.window_height / 15)))
            btn.setFixedSize(int(self.window_width / 16), int(self.window_height / 9.6))
            btn.setStyleSheet("border: none; background-color: transparent;")
            btn.clicked.connect(lambda _, idx=i: self.on_menu_item_clicked(idx))
            self.buttons.append(btn)
            btn.enterEvent = lambda event, b=btn: self.on_upper_hover_enter(b)
            btn.leaveEvent = lambda event, b=btn: self.on_upper_hover_leave(b)
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
            if callable(menu_action):
                menu_action()  # Calls the settings function if selected
            else:
                self.enum = 2
                os.chdir(os.path.dirname(menu_action))
                subprocess.run(["python", os.path.basename(menu_action)])
                os.chdir(self.gui_path)
                self.enum = 0
        except Exception as e:
            print(f"Chyba při spuštění menu: {e}")

    def settings(self):
        print("Settings function triggered.")
        for button in self.buttons:
            button.hide()

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
