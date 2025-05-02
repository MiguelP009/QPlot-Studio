from setuptools import setup

APP = ['QPlot-Studio.py']
DATA_FILES = ['data.json']  # ajoute ici d'autres fichiers à inclure
OPTIONS = {
    'argv_emulation': True,
    'packages': ['matplotlib', 'PySide6'],
    'includes': ['PySide6.QtWidgets', 'PySide6.QtCore', 'PySide6.QtGui'],
    'iconfile': 'icon.icns',  # optionnel, si tu as une icône
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
