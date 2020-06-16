### Dependencies ###
    matplotlib -> For tk ploting
    Microsoft Visual C++ Build Tools -> Needed by matplotlib and numpy
    pathlib
    screeninfo
    sympy -> For some math libs
    pyinstaller --> For binary executable creation. Needs to be compiled on the platform of destination, cross compiling for diferent platforms not supported!

###Compiling###
On windows 10:
    python -m PyInstaller .\main.py --onefile --name=Integrate -w

On Linux:
    python -m PyInstaller .\main.py --onefile --name=Integrate -w
