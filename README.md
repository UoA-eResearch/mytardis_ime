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
This project uses [poetry](https://python-poetry.org/).
Set up Poetry, then run:
```
poetry install
poetry shell # This activates the virtual envrionment
python -m app
``` 
Note:
If you are using an M1 Macbook, you need to install PyQt5 by creating a virtual environment and install PyQt5 using Rosetta Terminal.
To enable Rosetta on Terminal, the link might be useful: https://vineethbharadwaj.medium.com/m1-mac-switching-terminal-between-x86-64-and-arm64-e45f324184d9

```
env /usr/bin/arch -x86_64 /bin/zsh --login
arch
```
Set up your default Python version to 3.9.X by following https://towardsdatascience.com/how-to-use-manage-multiple-python-versions-on-an-apple-silicon-m1-mac-d69ee6ed0250
```
poetry install
source .venv/bin/activate
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