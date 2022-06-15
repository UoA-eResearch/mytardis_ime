import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWizard, QWizardPage, QVBoxLayout, QLabel
from PyQt5 import uic
from mainwindow import Ui_MainWindow
from models import Project, Experiment, Dataset, Datafile, FileInfo


class MyTardisMetadataEditor(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    window = uic.loadUi('MainWindow.ui')
    window.show()
    # window.show()
    sys.exit(app.exec_())
