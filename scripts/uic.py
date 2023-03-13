#!/usr/bin/env python
"""
uic.py - This script watches all ui files and generates corresponding
python files.
"""
import glob
import os
from PyQt5 import uic
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent, FileCreatedEvent

class UiFileModifiedHandler(PatternMatchingEventHandler):
    """
    A subclass of `PatternMatchingEventHandler` that handles modifications
    to UI files.

    Attributes:
        None

    Methods:
        on_created(event: FileCreatedEvent): Called when a new file is created.
            Compiles the UI file to Python code.
        on_modified(event: FileModifiedEvent): Called when a file is modified.
            Compiles the UI file to Python code.
    """
    def __init__(self) -> None:
        super().__init__(["**/*.ui"],ignore_directories=True)
    
    def on_created(self, event: FileCreatedEvent):
        """
        Called when a new file is created. Compiles the UI file to Python code.

        Args:
            event (FileCreatedEvent): The event object for the created file.

        Returns:
            None
        """
        fpath = event.src_path
        print("Generating python file for new file " + fpath)
        compile_ui_file(fpath)

    def on_modified(self, event: FileModifiedEvent):
        """
        Called when a file is modified. Compiles the UI file to Python code.

        Args:
            event (FileModifiedEvent): The event object for the modified file.

        Returns:
            None
        """
        fpath = event.src_path
        print("Generating python file for modified file " + fpath)
        compile_ui_file(fpath)

def compile_ui_file(fpath: str):
    """
    Compiles a UI file to Python code and saves it as a new file.

    Args:
        fpath (str): The file path of the UI file.

    Returns:
        None
    """
    fname = os.path.splitext(fpath)[0]
    with open(fname + '.py', 'w') as pyfile:
        try:
            uic.compileUi(fpath, pyfile)
        except:
            print("Error generating python file for " + fpath)

def compile_initial():
    """
    Compiles all existing UI files in the current directory and its subdirectories
    to Python code and saves them as new files.

    Args:
        None

    Returns:
        None
    """
    for f in glob.glob("**/*.ui", recursive=True):
        print("Generating python file for " + f)
        compile_ui_file(f)

def watch_and_compile(fpath):
    """
    Watches UI files for modifications and compiles them to Python code.

    Args:
        fpath (str): The file path to watch for modifications.

    Returns:
        None
    """
    handler = UiFileModifiedHandler()
    observer = Observer()
    observer.schedule(handler, fpath, recursive = True)
    observer.start()
    print("Watching .ui files for changes... Ctrl + C to quit.")
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    compile_initial()
    watch_and_compile('.')