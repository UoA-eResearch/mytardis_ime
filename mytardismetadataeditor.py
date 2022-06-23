from fileinput import filename
from importlib.metadata import files
from os import fpathconf
import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QWizard, QTableWidget, QTableWidgetItem, QLineEdit,QWizardPage, QVBoxLayout, QLabel,QFileDialog, QTreeWidget,QTreeWidgetItem
from PyQt5 import uic,QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QPersistentModelIndex,QModelIndex
from isort import file
import yaml
# from mainwindow import Ui_MainWindow
import models

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # load the ui file
        uic.loadUi('MainWindow.ui', self)

        # define our widgets
        self.actionImport_data_files.triggered.connect(self.openWizardWindow)
        #self.actionSave.triggered.connect(self.save_to_yaml)
        self.show()

    # Need to modify to enable file/dataset... sizes displaying
    @QtCore.pyqtSlot('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')
    def reFresh(self,project_info, experiment_info, dataset_info, datafile_info):
        self.project,self.experiment,self.dataset,self.datafile = project_info, experiment_info, dataset_info, datafile_info 
        l1 = QTreeWidgetItem([self.dataset.dataset_name,"1",self.experiment.experiment_name])
        l2 = QTreeWidgetItem([self.experiment.experiment_name,"3",self.project.project_name])
        l3 = QTreeWidgetItem([self.project.project_name,"4"])
        
        for file in self.datafile.files:
            l1_child = QTreeWidgetItem([file,"",""])
            l1.addChild(l1_child)
        self.datasetTreeWidget.addTopLevelItem(l1)
        self.experimentTreeWidget.addTopLevelItem(l2)
        self.projectTreeWidget.addTopLevelItem(l3)

    def openWizardWindow(self):  
        self.ui = WindowWizard()
        self.ui.submitted.connect(self.reFresh)
        self.ui.show()

    # Save to yaml files
    #@QtCore.pyqtSlot('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')
    #def save_to_yaml(self,project_info, experiment_info, dataset_info, datafile_info):
    #    with open('test/test_libby.yaml') as f:
    #        metadata = [project_info, experiment_info, dataset_info, datafile_info]
    #        yaml.dump_all(metadata,f)

class WindowWizard(QWizard):

    submitted = QtCore.pyqtSignal('PyQt_PyObject','PyQt_PyObject','PyQt_PyObject','PyQt_PyObject')

    def __init__(self):
        super(QWizard, self).__init__()
        uic.loadUi('add-files-wizard.ui', self)

        # define out widgets
        self.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        table = self.datafiletableWidget
        rows = self.open_dialog_box()
        self.addTableRow(table,rows)

    def deleteFiles_handler(self):
        index_list = []
        for model_index in self.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.datafiletableWidget.removeRow(index.row())

    def fpath(self):
        return self._fpath

    def open_dialog_box(self):
        filename_mode = QFileDialog()
        filename_mode.setFileMode(QFileDialog.ExistingFiles)
        filename = filename_mode.getOpenFileNames(self, "Open files")  
        fpath = filename[0]
        self._fpath = fpath
        def convert_bytes(size):
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0
        newrows = []
        for f in self._fpath:
            if f !="":
                info = QtCore.QFileInfo(f)
                size = info.size()
                fname = info.fileName()
                size_converted = convert_bytes(size)
            newrow = [fname,size_converted, f]
            if newrow not in newrows:
                newrows.append(newrow)
            else:
                continue
        return newrows
    
    def addTableRow(self,table,row_data):
        for lines in row_data:
            row = table.rowCount()
            table.setRowCount(row+1)
            col = 0
            for item in lines:
                cell = QTableWidgetItem(str(item))
                table.setItem(row, col, cell)
                col += 1
    
    def on_submit(self):
        project_info = models.Project()
        experiment_info = models.Experiment()
        dataset_info = models.Dataset()
        datafile_info = models.Datafile()

        project_info.project_name = self.projectNameLineEdit.text()
        project_info.project_id = self.projectIDLineEdit.text()
        project_info.description = self.projectDescriptionLineEdit.text()
        experiment_info.experiment_name = self.experimentNameLineEdit.text()
        experiment_info.experiment_id = self.experimentIDLineEdit.text()
        experiment_info.description = self.experimentdescriptionLineEdit.text()
        dataset_info.dataset_name = self.datasetNameLineEdit.text()
        dataset_info.dataset_id = self.instrumentIDLineEdit.text()

        table = self.datafiletableWidget
        file_list = []
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            if file_name not in file_list:
                file_list.append(file_name)
            else:
                continue

        datafile_info.files = file_list

        self.submitted.emit(project_info, experiment_info, dataset_info, datafile_info)
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())
