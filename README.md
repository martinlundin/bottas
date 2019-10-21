# Bottas

## Install 
Requirements: Python 3.6, Tesseract (and Homebrew to install it)
1. Install Homebrew
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
1. Install tesseract
`brew install tesseract && brew install tesseract-lang`
1. In project root run
`source venv/bin/activate`
1. Install requirements
`pip3 install -r requirements.txt`

**That's it**

## Running program:
1. Always activate venv
`source venv/bin/activate`
1. Run main.py
`python3 main.py`

**Note!**  This is Tested for Android Emulator, Nexus 5X.
Nexus emulator should be placed to the absolute top left of active screen.
The size should be equal to the program window. See screenshot:
![Alt text](img/alignments.png?raw=true "Size and alignments")

In bing.py, use premium key, or use dev = true. Or key will get blocked in a few tries.