PyInstaller --onefile ./example.py
copy /y dist\example.exe .\example.exe
del __pycache__
del PokerTestGame.exe.spec