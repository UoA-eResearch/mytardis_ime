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
    def __init__(self) -> None:
        super().__init__(["**/*.ui"],ignore_directories=True)
    
    def on_created(self, event: FileCreatedEvent):
        fpath = event.src_path
        print("Generating python file for new file " + fpath)
        compile_ui_file(fpath)

    def on_modified(self, event: FileModifiedEvent):
        fpath = event.src_path
        print("Generating python file for modified file " + fpath)
        compile_ui_file(fpath)

def compile_ui_file(fpath: str):
    fname = os.path.splitext(fpath)[0]
    with open(fname + '.py', 'w') as pyfile:
        try:
            uic.compileUi(fpath, pyfile)
        except:
            print("Error generating python file for " + fpath)

def compile_initial():
    for f in glob.glob("**/*.ui", recursive=True):
        print("Generating python file for " + f)
        compile_ui_file(f)

def watch_and_compile(fpath):
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