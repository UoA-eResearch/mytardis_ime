# Instrument Data Wizard
A metadata editor for files being ingested into MyTardis. Written with PyQt and PyYAML.

# Folder structure
```
    ime - Namespace for the package
    - ui - Qt UI files and generated PyQt Python files
    - widgets - Python code for individual custom widgets
    - tests - test suite for the project. Each test file has to start with test_.
    resources - Assets used in the UI.
    docs - user and developer documentation.
    scripts - scripts used for devlopment
    dist - generated executable.
```


# Set up for development
This project uses [poetry](https://python-poetry.org/).
Set up Poetry, then run:
```
poetry install
poetry run python -m app
``` 

This will install all the project dependencies, then run the app in the Python virtual environment created by `poetry`. 

If you need to run a command in the created virtual environment, you need to prepend the command with `poetry run`. Or, you can run `poetry shell` to spawn a shell with the virtual environment activated. This means all subsequent commands will be run in the virtual environment.


# UI files
You can automate the generation of PyQt Python files from `.ui` files by running:
```
./scripts/uic.py
```  
The script will watch `.ui` files and regenerate Python files when changed.

# Tests
This project uses [Pytest](https://www.pytest.org/). Run tests using:
```
poetry run pytest
```

# Documentation
This project uses [Sphinx](https://www.sphinx-doc.org/) to generate user and developer documentation. Run:
```
cd docs
poetry run make html
```

The resulting HTML documentation is available in the `docs/_build/html` directory.

# Generating executables
This project uses [pyinstaller](https://pypi.org/project/pyinstaller/) to generate a compiled executable. To use, run:
```
poetry run pyinstaller app.py
```