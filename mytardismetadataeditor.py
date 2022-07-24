import os, sys
from typing import List
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QToolBar, QAction, QWizard, QTableWidget, QTableWidgetItem, QLineEdit,QWizardPage, QVBoxLayout, QLabel,QFileDialog, QTreeWidget,QTreeWidgetItem
from PyQt5.QtCore import QPersistentModelIndex,QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from isort import file
import yaml

from ui.MainWindow import Ui_MainWindow
from ui.AddFilesWizard import Ui_ImportDataFiles
from models import IngestionMetadata, Project, Experiment, Dataset, Datafile, FileInfo
import logging
# Import the resources file
import default_rc

def file_size_to_str(size: float) -> str:
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        # If size exceeds 1024 TB, return in terms of TB.
        return "%3.1f %s" % (size, "TB")

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # load the ui file
        # uic.loadUi('MainWindow.ui', self)
        
        self.metadata = IngestionMetadata()

        # define our widgets
        self.ui.actionImport_data_files.triggered.connect(self.openWizardWindow)
        self.ui.actionSave.triggered.connect(self.save_to_yaml)

        self.ui.datasetTreeWidget.itemClicked.connect(self.onClickedDataset)
        self.ui.experimentTreeWidget.itemClicked.connect(self.onClickedExperiment)
        self.ui.projectTreeWidget.itemClicked.connect(self.onClickedProject)

        self.show()

    def onSelectDataset(self, item_id: str):
        # First, look up the dataset value
        dataset_lookup = [
            dataset
            for dataset in self.metadata.datasets
            if dataset.dataset_id == item_id
        ]
        if (len(dataset_lookup) != 1):
            logging.warning("Dataset ID %s could not be found or there are" + 
            "more than one entries.", item_id)
        dataset = dataset_lookup[0]
        # Set controls with value
        self.ui.datasetNameLineEdit.setText(dataset.dataset_name)
        self.ui.datasetIDLineEdit.setText(dataset.dataset_id)
        self.ui.instrumentIDLineEdit.setText(dataset.instrument_id)

    def onSelectDatafile(self, dataset_id: str, file_name: str):
        # First, look up the dataset value
        datafile_lookup = [
            datafile
            for datafile in self.metadata.datafiles
            if datafile.dataset_id == dataset_id
        ]
        if (len(datafile_lookup) != 1):
            logging.warning("Dataset ID %s could not be found or there are" + 
            "more than one entries.", dataset_id)
        datafile = datafile_lookup[0]
        # Next, look up FileInfo
        fileinfo_lookup = [
            fileinfo
            for fileinfo in datafile.files
            if fileinfo.name == file_name
        ]
        if (len(fileinfo_lookup) != 1):
            logging.warning("Datafile name %s could not be found or there are " + 
            "more than one entries.", file_name)
        fileinfo = fileinfo_lookup[0]
        # Set controls with value
        self.ui.fileInfoFilenameLineEdit.setText(fileinfo.name)


    def onClickedDataset(self):
            item: QTreeWidgetItem = self.ui.datasetTreeWidget.currentItem()
            item_id = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            props_widget : QStackedWidget = self.ui.datasetTabProps
            if item.parent() is None:
                # This indicates we are looking at a dataset,
                # change stacked widget to show dataset properties
                props_widget.setCurrentIndex(0)
                self.onSelectDataset(item_id)
            else:
                parent = item.parent()
                dataset_id = parent.data(0, QtCore.Qt.ItemDataRole.UserRole)
                props_widget.setCurrentIndex(1)
                self.onSelectDatafile(dataset_id, item_id)


            #self.instrumentIDLineEdit.setText(self.metadata.datasets.instrument_id)

    def onClickedExperiment(self):
            item = self.ui.experimentTreeWidget.currentItem()
            #print("Key=%s,value=%s"%(item.text(0),item.text(1)))
            self.ui.experimentNameLineEdit.setText(item.text(0))
            props_widget : QStackedWidget = self.ui.experimentTabProps
            props_widget.setCurrentIndex(0)
            #print(self.metadata)
            for ds in self.metadata.experiments:
                if ds.experiment_name == item.text(0):
                    self.ui.experimentIDLineEdit.setText(ds.experiment_id)
                    self.ui.experimentDescriptionLineEdit.setText(ds.description)
                else:
                    continue

    def onClickedProject(self):
            item = self.ui.projectTreeWidget.currentItem()
            props_widget : QStackedWidget = self.ui.projectTabProps
            props_widget.setCurrentIndex(0)

            #print("Key=%s,value=%s"%(item.text(0),item.text(1)))
            self.ui.projectNameLineEdit.setText(item.text(0))
            #print(self.metadata)
            for ds in self.metadata.projects:
                if ds.project_name == item.text(0):
                    self.ui.projectIDLineEdit.setText(ds.project_id)
                    self.ui.projectDescriptionLineEdit.setText(ds.description)
                else:
                    continue

    def reFresh(self,project_info: Project, experiment_info: Experiment, dataset_info: Dataset, datafile_info: Datafile):
        self.metadata.projects.append(project_info)
        self.metadata.experiments.append(experiment_info)
        self.metadata.datasets.append(dataset_info)
        self.metadata.datafiles.append(datafile_info)

        l1 = QTreeWidgetItem([dataset_info.dataset_name,dataset_info.metadata['Size'],experiment_info.experiment_name])
        l1.setData(0, QtCore.Qt.ItemDataRole.UserRole, dataset_info.dataset_id)

        l2 = QTreeWidgetItem([experiment_info.experiment_name,experiment_info.metadata['Size'],project_info.project_name])
        l2.setData(0, QtCore.Qt.ItemDataRole.UserRole, experiment_info.experiment_id)

        l3 = QTreeWidgetItem([project_info.project_name,project_info.metadata['Size']])
        l3.setData(0, QtCore.Qt.ItemDataRole.UserRole, project_info.project_id)
        

        for file in datafile_info.files:
            file_name = file.name
            file_size = file.metadata['Size']
            l1_child = QTreeWidgetItem([file_name,file_size,""])
            l1_child.setData(0, QtCore.Qt.ItemDataRole.UserRole, file_name)
            l1.addChild(l1_child)
        self.ui.datasetTreeWidget.addTopLevelItem(l1)
        self.ui.experimentTreeWidget.addTopLevelItem(l2)
        self.ui.projectTreeWidget.addTopLevelItem(l3)

    def openWizardWindow(self):  
        self.import_wizard_ui = WindowWizard()
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()
    
    # Save to yaml files
    def save_to_yaml(self):
        filename = QFileDialog.getSaveFileName(self,"Save File",directory = "test.yaml", initialFilter='Yaml File(*.yaml)')[0]
        if filename:
            with open(filename, 'w') as file:
                file.write(self.metadata.to_yaml())

class WindowWizard(QWizard):

    submitted = QtCore.pyqtSignal(Project, Experiment, Dataset, Datafile)

    def __init__(self):
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles()
        self.ui.setupUi(self)
        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB

    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        filename = file_dialog.getOpenFileNames(self, "Open files")  
        fpath = filename[0]

        new_files = []
        for f in fpath:
            if f == "":
                continue
            info = QtCore.QFileInfo(f)
            if info in new_files:
                continue
            new_files.append(info)
        return new_files
    
    def add_file_table_rows(self,table: QTableWidget,files_to_add: List[QtCore.QFileInfo]) -> None:
        # Need to start inserting rows after existing rows.
        initial_row_count = table.rowCount()
        # Grow the table to fit new rows.
        table.setRowCount(initial_row_count + len(files_to_add))
        new_row_index = 0
        for file in files_to_add:
            # Create corresponding cells for file and insert them into table.
            name_cell = QTableWidgetItem(file.fileName())
            size = file.size()
            size_str = file_size_to_str(size)
            size_cell = QTableWidgetItem(size_str)
            # Store actual size value in cell. 
            size_cell.setData(QtCore.Qt.ItemDataRole.UserRole, size)
            fpath_cell = QTableWidgetItem(file.filePath())
            # Insert cells into the table.
            row_index = initial_row_count + new_row_index
            table.setItem(row_index, 0, name_cell)
            table.setItem(row_index, 1, size_cell)
            table.setItem(row_index, 2, fpath_cell)
            # Increment for the next row
            new_row_index += 1
    
    def on_submit(self):
        project_info = Project()
        experiment_info = Experiment()
        dataset_info = Dataset()
        datafile_info = Datafile()

        project_info.project_name = self.ui.projectNameLineEdit.text()
        project_info.project_id = self.ui.projectIDLineEdit.text()
        project_info.description = self.ui.projectDescriptionLineEdit.toPlainText()
        experiment_info.experiment_name = self.ui.experimentNameLineEdit.text()
        experiment_info.experiment_id = self.ui.experimentIDLineEdit.text()
        experiment_info.project_id = self.ui.projectIDLineEdit.text()
        experiment_info.description = self.ui.experimentDescriptionLineEdit.toPlainText()
        dataset_info.dataset_name = self.ui.datasetNameLineEdit.text()
        dataset_info.dataset_id = self.ui.datasetIDLineEdit.text()
        # Because a dataset can belong to multiple experiments,
        # we are creating a list around the experiment we captured.
        dataset_info.experiment_id = [self.ui.experimentIDLineEdit.text()]

        datafile_info.dataset_id = dataset_info.dataset_id

        table = self.ui.datafiletableWidget
        # Calculate the size of dataset, experiment, project.
        total_size = 0
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            file_info = FileInfo(name = file_name)
            file_info.size = size
            datafile_info.files.append(file_info)
            total_size += size

        # Add the total size of the datafiles to projects, experiments and datasets they belong to.
        dataset_info.size += total_size
        experiment_info.size += total_size
        project_info.size += total_size

        self.submitted.emit(project_info, experiment_info, dataset_info, datafile_info)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())
