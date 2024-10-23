from setuptools import setup

APP = ['/Users/tomasfikart/PycharmProjects/pythonProject/games/SpaceShooter/game_files/main.py']  # Nastav správnou cestu k hlavnímu souboru
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
