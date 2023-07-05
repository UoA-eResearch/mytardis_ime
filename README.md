# Instrument Data Wizard
A metadata editor for files being ingested into MyTardis. Written with PyQt and PyYAML.

# Folder structure
```
    ime - Namespace for the package
    - ui - Qt UI files and generated PyQt Python files
    - widgets - Python code for individual custom widgets
    - tests - test suite for the project. Each test file has to start with test_.
    resources - Assets used in the UI.
    scripts - scripts used for devlopment
    dist - generated executable.
```


# Set up for development
In order to run the image metadata extraction scripts, your device needs JAVA installed. Download [Java JDK](https://www.oracle.com/nz/java/technologies/downloads/#jdk20-linux)

This project uses [poetry](https://python-poetry.org/).
Set up Poetry, then run:
```
poetry install
poetry shell # This activates the virtual envrionment
python -m app
``` 
Note:
If you are using an M1 Macbook, you need to install PyQt5 by using Rosetta Terminal.
To enable Rosetta on Terminal, the link might be useful: https://vineethbharadwaj.medium.com/m1-mac-switching-terminal-between-x86-64-and-arm64-e45f324184d9

```
env /usr/bin/arch -x86_64 /bin/zsh --login
arch
```
Then you can: 
Set up Poetry, and run:
```
poetry install
poetry shell # This activates the virtual envrionment
python -m app
``` 

## UI files
You can automate the generation of PyQt Python files from `.ui` files by running:
```
./scripts/uic.py
```  
The script will watch `.ui` files and regenerate Python files when changed.

# Tests
Ensure you're in the Poetry virtual environment, run tests using:
```
pytest
```

# Generating executables
This project uses [pyinstaller](https://pypi.org/project/pyinstaller/) to generate a compiled executable. To use, ensure you're in the Poetry virtual environment, then run:
```
pyinstaller app.py
```