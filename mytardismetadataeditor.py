from fileinput import filename
from os import fpathconf
import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QWizard, QTableWidget, QTableWidgetItem, QWizardPage, QVBoxLayout, QLabel,QFileDialog
from PyQt5 import uic,QtWidgets,QtCore,QtGui
# from mainwindow import Ui_MainWindow
import models

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # load the ui file
        uic.loadUi('MainWindow.ui', self)

        # define our widgets
        #self.actionImport_data_files = self.findChild(QAction, "actionImport_data_files")
        self.actionImport_data_files.triggered.connect(self.openWindow)
        self.show()

    def openWindow(self):  
        self.ui = WindowWizard()
        self.ui.show()

class WindowWizard(QWizard):
    def __init__(self):
        super(QWizard, self).__init__()
        uic.loadUi('add-files-wizard.ui', self)

        # define out widgets
        self.datafilepushButton.clicked.connect(self.addFiles_handler)

    def addFiles_handler(self):
        self.open_dialog_box()

    def fpath(self):
        return self._fpath

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        fpath = filename[0]
        self._fpath = fpath
        def convert_bytes(size):
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0
        if filename !="":
            info = QtCore.QFileInfo(self._fpath)
            size = info.size()
            fname = info.fileName()
            size_converted = convert_bytes(size)
        newrow = [size_converted, fname]
        table = self.datafiletableWidget
        self.addTableRow(table,newrow)
    
    def addTableRow(self,table,row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1




if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())
