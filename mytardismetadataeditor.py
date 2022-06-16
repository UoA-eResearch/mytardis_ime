from fileinput import filename
from os import fpathconf
import sys
<<<<<<< HEAD
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QWizard, QWizardPage, QVBoxLayout, QLabel,QFileDialog
from PyQt5 import uic,QtWidgets,QtCore,QtGui
# from mainwindow import Ui_MainWindow

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # load the ui file
        uic.loadUi('MainWindow.ui', self)

        # define our widgets
        self.actionImport_data_files = self.findChild(QAction, "actionImport_data_files")
        self.actionImport_data_files.triggered.connect(self.openWindow)
        self.show()

    def openWindow(self):  
        self.ui = WindowWizard()
        self.ui.show()
###        self.close()

class WindowWizard(QWizard):
    def __init__(self):
        super(QWizard, self).__init__()
        uic.loadUi('add-files-wizard.ui', self)

        # define out widgets
        self.datafilepushButton.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self):
        self.open_dialog_box()

    def fpath(self):
        return self._fpath

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self._fpath = path
'''
    def verify_input_data_file(self):
        alert = QtWidgets.QMessageBox()
        alert.setText('The input filepath you selected is: \n{}'.format(self.fpath))
        alert.exec_()
        # alert.close()
        # alert = None
'''        

'''
    def onTextChanged(self,text):
        settings = QtCore.QSettings()
        settings.setValue("text", text)
    def onClicked(self):
        settings  =QtCore.QSettings()
        text = settings.value("text")
        print(text)
''' 

=======
from PyQt5.QtWidgets import QApplication, QMainWindow, QWizard, QWizardPage, QVBoxLayout, QLabel
from PyQt5 import uic
from mainwindow import Ui_MainWindow
from models import IngestionMetadata

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        # Initialise the app ingestion metadata state.
        self.metadata = IngestionMetadata()
        QMainWindow.__init__(self)

>>>>>>> 49e064d2ecffead54c07436d560d234329dd3945
if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())
