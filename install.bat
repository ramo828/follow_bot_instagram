@echo off

pip install -r requirements.txt
pyinstaller --onefile main.py --icon icon.ico --noconsole

PAUSE